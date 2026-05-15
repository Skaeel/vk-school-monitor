def wall_get_script(domains: list):
    script = f"""
    var domains = {domains};
    var results = [];
    var i = 0;

    while (i < domains.length) {{
        var posts = API.wall.get({{
            "domain": domains[i],
            "count": 100,
            "filter": "owner"
        }});
        if (posts.items) {{
            results.push(posts.items);
        }}
        i = i + 1;
    }}
    return results;
    """
    return script