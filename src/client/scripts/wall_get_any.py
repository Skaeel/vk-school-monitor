def wall_get_any(domains: list):
    script = f"""
    var domains = {domains};
    var results = [];
    var i = 0;

    while (i < domains.length) {{
        var posts = API.wall.get({{
            "domain": domains[i],
            "count": 100,
            "filter": "all"
        }});
        results.push(posts);
        i = i + 1;
    }}
    return results;
    """
    return script