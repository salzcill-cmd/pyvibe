"""
PyVibe Navigation & SEO — Unit Tests

Tests for: SEO, SitemapGenerator, RobotsGenerator, use_params, use_query, build_url, redirect
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyvibe.navigation import (
    SEO, SitemapGenerator, RobotsGenerator,
    use_params, use_query, build_url, redirect,
    Router, RouteMeta,
)

passed = 0
failed = 0
total = 0


def test(name, condition, expected="", got=""):
    global passed, failed, total
    total += 1
    if condition:
        passed += 1
        print(f"  ✅ {name}")
    else:
        failed += 1
        print(f"  ❌ {name}")
        if expected or got:
            print(f"     Expected: {expected}")
            print(f"     Got: {got}")


print("=" * 70)
print("🧭 PyVibe Navigation & SEO — Unit Tests")
print("=" * 70)

# ==================== SEO ====================
print("\n--- SEO ---")

seo = SEO(
    title="My Page | MySite",
    description="This is a description",
    image="https://example.com/og.png",
    url="https://example.com/page",
    site_name="MySite",
    keywords=["python", "web", "framework"],
    author="PyVibe Team",
)

html = seo.render()
test("SEO render returns string", isinstance(html, str))
test("SEO has og:title", "og:title" in html)
test("SEO has og:description", "og:description" in html)
test("SEO has og:image", "og:image" in html)
test("SEO has og:url", "og:url" in html)
test("SEO has og:type", "og:type" in html)
test("SEO has og:site_name", "og:site_name" in html)
test("SEO has keywords", "keywords" in html)
test("SEO has author", "author" in html)
test("SEO has title tag", "<title>" in html)

seo_minimal = SEO()
html_min = seo_minimal.render()
test("SEO minimal render", isinstance(html_min, str))

og_html = seo.render_og()
test("SEO render_og", "og:title" in og_html)

# ==================== SEO Structured Data ====================
print("\n--- SEO Structured Data ---")

seo_sd = SEO(
    title="Article",
    structured_data={
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Test Article",
    }
)
html_sd = seo_sd.render()
test("SEO structured data", "application/ld+json" in html_sd)
test("SEO structured data content", "Article" in html_sd)

# ==================== SEO HTML Escaping ====================
print("\n--- SEO HTML Escaping ---")

seo_escape = SEO(title='Test <script>alert("xss")</script>')
html_esc = seo_escape.render()
test("SEO escapes HTML", "<script>" not in html_esc)
test("SEO escapes quotes", '&quot;' in html_esc or "script" not in html_esc)

# ==================== SitemapGenerator ====================
print("\n--- SitemapGenerator ---")

sitemap = SitemapGenerator("https://example.com")
sitemap.add("/", priority=1.0, changefreq="daily")
sitemap.add("/about", priority=0.8, changefreq="monthly")
sitemap.add("/blog", priority=0.9, changefreq="weekly")

xml = sitemap.render()
test("Sitemap render returns string", isinstance(xml, str))
test("Sitemap has urlset", "<urlset" in xml)
test("Sitemap has URLs", "https://example.com/" in xml)
test("Sitemap has priority", "<priority>1.0" in xml)
test("Sitemap has changefreq", "<changefreq>daily" in xml)
test("Sitemap has multiple URLs", xml.count("<url>") == 3)

sitemap_empty = SitemapGenerator("https://test.com")
xml_empty = sitemap_empty.render()
test("Sitemap empty", "<urlset" in xml_empty)
test("Sitemap empty no URLs", "<url>" not in xml_empty)

# ==================== RobotsGenerator ====================
print("\n--- RobotsGenerator ---")

robots = RobotsGenerator(sitemap_url="https://example.com/sitemap.xml")
robots.allow("/", "*")
robots.disallow("/admin", "*")
robots.disallow("/private", "Googlebot")

txt = robots.render()
test("Robots render returns string", isinstance(txt, str))
test("Robots has User-agent", "User-agent" in txt)
test("Robots has Allow", "Allow: /" in txt)
test("Robots has Disallow", "Disallow: /admin" in txt)
test("Robots has Sitemap", "Sitemap:" in txt)

robots_empty = RobotsGenerator()
txt_empty = robots_empty.render()
test("Robots empty", isinstance(txt_empty, str))

# ==================== use_params ====================
print("\n--- use_params ---")

params = use_params("/users/:id", "/users/123")
test("use_params simple", params == {"id": "123"})

params2 = use_params("/users/:id/posts/:post_id", "/users/456/posts/789")
test("use_params multiple", params2 == {"id": "456", "post_id": "789"})

params3 = use_params("/page/:slug", "/page/hello-world")
test("use_params slug", params3 == {"slug": "hello-world"})

params_empty = use_params("/static", "/static")
test("use_params no params", params_empty == {})

params_none = use_params("/users/:id", "/different/path")
test("use_params no match", params_none == {})

# ==================== use_query ====================
print("\n--- use_query ---")

query = use_query("/search?q=python&page=2")
test("use_query simple", "q" in query)
test("use_query page param", "page" in query)

query_empty = use_query("/page")
test("use_query no query", query_empty == {} or len(query_empty) == 0)

# ==================== build_url ====================
print("\n--- build_url ---")

url1 = build_url("/users/:id", params={"id": "123"})
test("build_url with params", url1 == "/users/123")

url2 = build_url("/search", query={"q": "python", "page": "2"})
test("build_url with query", "q=python" in url2)

url3 = build_url("/users/:id/posts/:post_id", params={"id": "1", "post_id": "2"})
test("build_url with multiple params", url3 == "/users/1/posts/2")

url4 = build_url("/page")
test("build_url no params", url4 == "/page")

# ==================== redirect ====================
print("\n--- redirect ---")

r = redirect("https://example.com")
test("redirect returns string", isinstance(r, str))
test("redirect has script tag", "<script>" in r)
test("redirect has url", "https://example.com" in r)

# ==================== Router ====================
print("\n--- Router ---")

router = Router()

def home_handler():
    return "home"

def about_handler():
    return "about"

router.add_route("/", home_handler)
router.add_route("/about", about_handler)

test("Router add_route", "/" in router.routes)
test("Router has handler", router.routes["/"]["handler"] == home_handler)

result = router.navigate("/")
test("Router navigate home", result["status"] == "ok")
test("Router current route", router.current_route["path"] == "/")

result2 = router.navigate("/about")
test("Router navigate about", result2["status"] == "ok")

result3 = router.navigate("/nonexistent")
test("Router navigate 404", result3["status"] == "error")

# Router guards
guard_called = [False]

@router.before_each
def guard(to, from_):
    guard_called[0] = True
    return True

router.navigate("/")
test("Router guard called", guard_called[0])

# Router back
router.navigate("/about")
result_back = router.back()
test("Router back", result_back["status"] == "ok")

# ==================== RouteMeta ====================
print("\n--- RouteMeta ---")

meta = RouteMeta(
    title="Test Page",
    description="Test description",
    requires_auth=True,
    requires_role="admin",
)
test("RouteMeta title", meta.title == "Test Page")
test("RouteMeta requires_auth", meta.requires_auth is True)
test("RouteMeta requires_role", meta.requires_role == "admin")

# ==================== Summary ====================
print("\n" + "=" * 70)
print(f"Results: {passed}/{total} tests passed")
if failed == 0:
    print("🎉 ALL NAVIGATION & SEO TESTS PASSED!")
else:
    print(f"⚠️ {failed} tests failed")
print("=" * 70)

sys.exit(0 if failed == 0 else 1)
