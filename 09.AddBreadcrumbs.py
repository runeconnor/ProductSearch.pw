import os

from includes.functions import php_add_slashes

root = "D:\\wamp64\\www"

# Traverse the entire site and find all meta.php files
meta_php_urls = []
for subdir, dirs, files in os.walk(root):
    for file in files:
        if file == 'meta.php':
            meta_php_urls.append(os.path.join(subdir, file))

breadcrumbs_php = """
<?php
# Breadcrumbs
$crumbs = explode('/',$_SERVER["REQUEST_URI"]);
$crumbs = array_filter($crumbs);
$link_texts = [];

foreach($crumbs as $key => $value) {
    $link_texts[$key] = ucfirst(str_replace(array(".php", "_", "-"), array("", " ", " "), $value) . ' ');
}

$path = $rootpath;

$breadcrumbs = "<div class=\\"breadcrumb\\"><ul><li><a href=";
$breadcrumbs .= $rootpath;
$breadcrumbs .= ">Home</a></li>";

foreach($crumbs as $key => $value){
    if ($path != $rootpath) {
        $path .= "/";
    }
    $path .= $value;
    $breadcrumbs .= "<li><a href=";
    $breadcrumbs .= $path;
    $breadcrumbs .= ">";
    $breadcrumbs .= $link_texts[$key];
    $breadcrumbs .= "</a></li>";
}
$breadcrumbs .= "</ul></div>"
?>"""

for url in meta_php_urls:
    with open(url.strip(), 'a', encoding='utf-8') as f:
        f.write(breadcrumbs_php)
        print(url.strip(), '-- OK')

