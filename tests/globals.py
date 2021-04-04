CONFIG = {"plugins": ["search"]}
TO_EXCLUDE = [
    "chapter_exclude_all.md",
    "chapter_exclude_heading2.md#single-header-chapter_exclude_heading2-bbex",
    "dir/dir_chapter_exclude_all.md",
    "dir/dir_chapter_ignore_heading3.md",
    "all_dir/*",
    "all_dir_sub/all_dir_sub2/*",
]

RESOLVED_EXCLUDED_RECORDS = [
    ("chapter_exclude_all.md", None),
    ("chapter_exclude_heading2.md", "single-header-chapter_exclude_heading2-bbex"),
    ("dir/dir_chapter_exclude_all.md", None),
    ("dir/dir_chapter_ignore_heading3.md", None),
    ("all_dir/*", None),
    ("all_dir_sub/all_dir_sub2/*", None),
]

TO_IGNORE = [
    "dir/dir_chapter_ignore_heading3.md#dir-single-header-dir_chapter_ignore_heading3-ccin",
    "all_dir/all_dir_ignore_heading1.md#alldir-header-all_dir_ignore_heading1-aain",
]

RESOLVED_IGNORED_CHAPTERS = [
    (
        "dir/dir_chapter_ignore_heading3.md",
        "dir-single-header-dir_chapter_ignore_heading3-ccin",
    ),
    (
        "all_dir/all_dir_ignore_heading1.md",
        "alldir-header-all_dir_ignore_heading1-aain",
    ),
    ("dir/dir_chapter_ignore_heading3.md", None),
    ("all_dir/all_dir_ignore_heading1.md", None),
]

EXCLUDE_TAGS = False

INCLUDED_RECORDS = [
    {"location": "", "text": "Index Hello, hello", "title": "index"},
    {"location": "#index", "text": "Hello, hello", "title": "Index"},
    {
        "location": "chapter_exclude_heading2/",
        "text": "single chapter_exclude_heading2 Header Ain single header chapter_exclude_"
        "heading2 AAin single text chapter_exclude_heading2 AAin single header "
        "chapter_exclude_heading2 BBex single text chapter_exclude_heading2 BBex",
        "title": "chapter_exclude_heading2",
    },
    {
        "location": "chapter_exclude_heading2/#single-chapter_exclude_heading2-header-ain",
        "text": "",
        "title": "single chapter_exclude_heading2 Header Ain",
    },
    {
        "location": "chapter_exclude_heading2/#single-header-chapter_exclude_heading2-aain",
        "text": "single text chapter_exclude_heading2 AAin",
        "title": "single header chapter_exclude_heading2 AAin",
    },
    {
        "location": "all_dir/all_dir_ignore_heading1/",
        "text": "alldir Header all_dir_ignore_heading1 Aex alldir header all_dir_ignore_"
        "heading1 AAin alldir text all_dir_ignore_heading1 AAin alldir header "
        "all_dir_ignore_heading1 BBex alldir text all_dir_ignore_heading1 BBex",
        "title": "all_dir_ignore_heading1",
    },
    {
        "location": "all_dir/all_dir_ignore_heading1/#alldir-header-all_dir_ignore_heading1-aain",
        "text": "alldir text all_dir_ignore_heading1 AAin",
        "title": "alldir header all_dir_ignore_heading1 AAin",
    },
    {
        "location": "dir/dir_chapter_ignore_heading3/",
        "text": "dir single Header dir_chapter_ignore_heading3 Aex dir single header "
        "dir_chapter_ignore_heading3 AAex dir single text dir_chapter_ignore_heading3 "
        "AAex dir single header dir_chapter_ignore_heading3 CCin dir single text "
        "dir_chapter_ignore_heading3 CCin",
        "title": "dir_chapter_ignore_heading3",
    },
    {
        "location": "dir/dir_chapter_ignore_heading3/#dir-single-header-dir_chapter_ignore_heading3-ccin",
        "text": "dir single text dir_chapter_ignore_heading3 CCin",
        "title": "dir single header dir_chapter_ignore_heading3 CCin",
    },
    {
        "location": "tags.html",
        "text": "Contents grouped by tag testing Welcome unimportant Welcome",
        "title": "Tags",
    },
    {
        "location": "tags.html#contents-grouped-by-tag",
        "text": "",
        "title": "Contents grouped by tag",
    },
    {"location": "tags.html#testing", "text": "Welcome", "title": "testing"},
    {"location": "tags.html#unimportant", "text": "Welcome", "title": "unimportant"},
]
