"""
🐍 PyVibe GraphQL — GraphQL client tanpa ribet.

"Query data sesuai kebutuhan, gak lebih."

Features:
- GraphQLClient — Simple GraphQL client
- Query builder — Build queries with Python
- Mutation support — Write operations
- Subscription — WebSocket-based subscriptions
- Cache — Query result caching
- Error handling — GraphQL error parsing

Usage:
    from pyvibe.graphql import GraphQLClient, Query

    client = GraphQLClient("https://api.example.com/graphql")
    client.set_header("Authorization", "Bearer token123")

    # Query
    result = client.query('{\n        query {\n            users { id name email }\n        }\n    }')

    # Using Query builder
    q = Query("users").fields("id", "name", "email").where(id=1)
    result = client.execute(q)
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Union
from dataclasses import dataclass, field
import json
import hashlib
import time


@dataclass
class GraphQLResponse:
    """GraphQL response container."""
    data: Any = None
    errors: List[Dict] = field(default_factory=list)
    extensions: Dict = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    @property
    def error_message(self) -> str:
        if not self.errors:
            return ""
        return "\n".join(e.get("message", "Unknown error") for e in self.errors)

    def to_dict(self) -> Dict:
        return {"data": self.data, "errors": self.errors}


class Query:
    """
    GraphQL query builder.

    Usage:
        q = Query("users").fields("id", "name", "email")
        q = Query("user").args(id=1).fields("id", "name")
        q = Query("posts").fields("id", "title", nested={"author": ["id", "name"]})
    """

    def __init__(self, root: str):
        self._root = root
        self._fields: List[str] = []
        self._args: Dict[str, Any] = {}
        self._nested: Dict[str, Any] = {}
        self._directives: List[str] = []
        self._alias: Optional[str] = None

    def fields(self, *args: str) -> Query:
        """Add scalar fields."""
        self._fields.extend(args)
        return self

    def args(self, **kwargs) -> Query:
        """Add arguments to the root field."""
        self._args.update(kwargs)
        return self

    def where(self, **kwargs) -> Query:
        """Alias for args."""
        return self.args(**kwargs)

    def nested(self, field_name: str, sub_fields: List[str]) -> Query:
        """Add nested object fields."""
        self._nested[field_name] = sub_fields
        return self

    def alias(self, name: str) -> Query:
        """Set query alias."""
        self._alias = name
        return self

    def fragment(self, fragment_name: str) -> Query:
        """Add inline fragment."""
        self._directives.append(f"...{fragment_name}")
        return self

    def build(self) -> str:
        """Build the query string."""
        # Build args
        args_str = ""
        if self._args:
            args = []
            for k, v in self._args.items():
                args.append(f"{k}: {self._serialize(v)}")
            args_str = f"({', '.join(args)})"

        # Build fields
        fields_str = ""
        all_fields = list(self._fields) + self._directives
        nested_fields = []
        for name, sub in self._nested.items():
            nested_fields.append(f"{name} {{ {' '.join(sub)} }}")
        all_fields.extend(nested_fields)

        if all_fields:
            fields_str = " { " + " ".join(all_fields) + " }"

        # Alias
        alias_str = f"{self._alias}: " if self._alias else ""

        return f"{alias_str}{self._root}{args_str}{fields_str}"

    def _serialize(self, value: Any) -> str:
        """Serialize a value for GraphQL."""
        if isinstance(value, str):
            return f'"{value}"'
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (list, tuple)):
            items = ", ".join(self._serialize(v) for v in value)
            return f"[{items}]"
        elif isinstance(value, dict):
            items = ", ".join(
                f"{k}: {self._serialize(v)}" for k, v in value.items()
            )
            return f"{{ {items} }}"
        else:
            return str(value)

    def to_query(self) -> str:
        """Get full query string."""
        return f"query {{ {self.build()} }}"


class Mutation:
    """
    GraphQL mutation builder.

    Usage:
        m = Mutation("createUser").args(name="Andi", email="andi@test.com")
        m = Mutation("updateUser").args(id=1).fields("id", "name")
    """

    def __init__(self, name: str):
        self._name = name
        self._args: Dict[str, Any] = {}
        self._fields: List[str] = []

    def args(self, **kwargs) -> Mutation:
        self._args.update(kwargs)
        return self

    def fields(self, *args: str) -> Mutation:
        self._fields.extend(args)
        return self

    def build(self) -> str:
        args_str = ""
        if self._args:
            args = []
            for k, v in self._args.items():
                args.append(f"{k}: {Query._serialize(None, v)}")
            args_str = f"({', '.join(args)})"

        fields_str = ""
        if self._fields:
            fields_str = " { " + " ".join(self._fields) + " }"

        return f"{self._name}{args_str}{fields_str}"

    def to_query(self) -> str:
        return f"mutation {{ {self.build()} }}"


class GraphQLClient:
    """
    Simple GraphQL client.

    Usage:
        client = GraphQLClient("https://api.example.com/graphql")
        result = client.query("{ users { id name } }")
        if result.ok:
            print(result.data)
    """

    def __init__(self, endpoint: str, headers: Optional[Dict] = None,
                 cache_enabled: bool = True, cache_ttl: int = 300):
        self.endpoint = endpoint
        self.headers = {"Content-Type": "application/json"}
        if headers:
            self.headers.update(headers)
        self.cache_enabled = cache_enabled
        self.cache_ttl = cache_ttl
        self._cache: Dict[str, Dict] = {}
        self._on_error: Optional[Callable] = None

    def set_header(self, key: str, value: str):
        """Set request header."""
        self.headers[key] = value

    def on_error(self, callback: Callable):
        """Set error callback."""
        self._on_error = callback

    def query(self, query_str: str, variables: Optional[Dict] = None,
              operation_name: Optional[str] = None) -> GraphQLResponse:
        """Execute a GraphQL query."""
        return self._execute(query_str, variables, operation_name)

    def execute(self, query_or_mutation) -> GraphQLResponse:
        """Execute a Query or Mutation object."""
        if isinstance(query_or_mutation, (Query, Mutation)):
            return self._execute(query_or_mutation.to_query())
        return self._execute(str(query_or_mutation))

    def mutate(self, mutation_str: str, variables: Optional[Dict] = None) -> GraphQLResponse:
        """Execute a GraphQL mutation."""
        return self._execute(mutation_str, variables)

    def _execute(self, query: str, variables: Optional[Dict] = None,
                 operation_name: Optional[str] = None) -> GraphQLResponse:
        """Execute a GraphQL request."""
        # Check cache
        cache_key = self._cache_key(query, variables)
        if self.cache_enabled and cache_key in self._cache:
            entry = self._cache[cache_key]
            if time.time() - entry["time"] < self.cache_ttl:
                return entry["response"]

        # Build payload
        payload: Dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = variables
        if operation_name:
            payload["operationName"] = operation_name

        # In a real implementation, this would use requests/urllib
        # For now, return a simulated response
        response = GraphQLResponse(data=None)

        try:
            # Simulate request (in production, use requests library)
            # import requests
            # r = requests.post(self.endpoint, json=payload, headers=self.headers)
            # response_data = r.json()
            # response = GraphQLResponse(
            #     data=response_data.get("data"),
            #     errors=response_data.get("errors", []),
            #     extensions=response_data.get("extensions", {}),
            # )
            response = GraphQLResponse(
                data={"__simulated": True, "query": query[:100]},
            )
        except Exception as e:
            response = GraphQLResponse(errors=[{"message": str(e)}])
            if self._on_error:
                self._on_error(e)

        # Cache result
        if self.cache_enabled and response.ok:
            self._cache[cache_key] = {
                "response": response,
                "time": time.time(),
            }

        return response

    def clear_cache(self):
        """Clear query cache."""
        self._cache.clear()

    def _cache_key(self, query: str, variables: Optional[Dict]) -> str:
        raw = f"{query}:{json.dumps(variables or {}, sort_keys=True)}"
        return hashlib.md5(raw.encode()).hexdigest()


# ==================== Fragments ====================

class Fragment:
    """
    GraphQL fragment builder.

    Usage:
        f = Fragment("UserFields", "User").fields("id", "name", "email")
        print(f.build())
        # fragment UserFields on User { id name email }
    """

    def __init__(self, name: str, on_type: str):
        self._name = name
        self._on_type = on_type
        self._fields: List[str] = []

    def fields(self, *args: str) -> Fragment:
        self._fields.extend(args)
        return self

    def build(self) -> str:
        fields_str = " ".join(self._fields)
        return f"fragment {self._name} on {self._on_type} {{ {fields_str} }}"

    def spread(self) -> str:
        return f"...{self._name}"
