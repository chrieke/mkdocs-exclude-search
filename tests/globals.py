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

EXCLUDE_UNREFERENCED = False
EXCLUDE_TAGS = False

NAVIGATION = [
    {"index": "index.md"},
    "without_nav_name.md",
    {"chapter_exclude_all": "chapter_exclude_all.md"},
    {
        "toplvl_chapter": [
            "toplvl_chapter/file_in_toplvl_chapter.md",
            {
                "sub_chapter": [
                    "toplvl_chapter/sub_chapter/file1_in_sub_chapter.md",
                    "toplvl_chapter/sub_chapter/file2_in_sub_chapter.md",
                ]
            },
        ]
    },
]

INCLUDED_RECORDS = [
    {"location": "", "text": "Index Hello, hello", "title": "index"},
    {"location": "#index", "text": "Hello, hello", "title": "Index"},
    {
        "location": "chapter_exclude_heading2/",
        "text": "single chapter_exclude_heading2 Header Ain single header chapter_exclude_heading2 "
        "AAin single text chapter_exclude_heading2 AAin single header chapter_exclude_heading2 "
        "BBex single text chapter_exclude_heading2 BBex",
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
        "location": "unreferenced/",
        "text": "unreferenced file heading1 Aex This is an example of an unreferenced file "
        "Unreferenced file heading2 AAex Unreferenced file heading2 BBex",
        "title": "unreferenced file heading1 Aex",
    },
    {
        "location": "unreferenced/#unreferenced-file-heading1-aex",
        "text": "This is an example of an unreferenced file",
        "title": "unreferenced file heading1 Aex",
    },
    {
        "location": "unreferenced/#unreferenced-file-heading2-aaex",
        "text": "",
        "title": "Unreferenced file heading2 AAex",
    },
    {
        "location": "unreferenced/#unreferenced-file-heading2-bbex",
        "text": "",
        "title": "Unreferenced file heading2 BBex",
    },
    {
        "location": "all_dir/all_dir_ignore_heading1/",
        "text": "alldir Header all_dir_ignore_heading1 Aex alldir header all_dir_ignore_heading1 "
        "AAin alldir text all_dir_ignore_heading1 AAin alldir header all_dir_ignore_heading1 "
        "BBex alldir text all_dir_ignore_heading1 BBex",
        "title": "all_dir_ignore_heading1",
    },
    {
        "location": "all_dir/all_dir_ignore_heading1/#alldir-header-all_dir_ignore_heading1-aain",
        "text": "alldir text all_dir_ignore_heading1 AAin",
        "title": "alldir header all_dir_ignore_heading1 AAin",
    },
    {
        "location": "dir/dir_chapter_ignore_heading3/",
        "text": "dir single Header dir_chapter_ignore_heading3 Aex dir single header dir_chapter_ignore_heading3 "
        "AAex dir single text dir_chapter_ignore_heading3 AAex dir single header dir_chapter_ignore_heading3 "
        "CCin dir single text dir_chapter_ignore_heading3 CCin",
        "title": "dir_chapter_ignore_heading3",
    },
    {
        "location": "dir/dir_chapter_ignore_heading3/#dir-single-header-dir_chapter_ignore_heading3-ccin",
        "text": "dir single text dir_chapter_ignore_heading3 CCin",
        "title": "dir single header dir_chapter_ignore_heading3 CCin",
    },
    {
        "location": "toplvl_chapter/file_in_toplvl_chapter/",
        "text": "Header file_in_toplvl_chapter text file_in_toplvl_chapter",
        "title": "Header file_in_toplvl_chapter",
    },
    {
        "location": "toplvl_chapter/file_in_toplvl_chapter/#header-file_in_toplvl_chapter",
        "text": "text file_in_toplvl_chapter",
        "title": "Header file_in_toplvl_chapter",
    },
    {
        "location": "toplvl_chapter/sub_chapter/file1_in_sub_chapter/",
        "text": "Header file1_in_sub_chapter text file1_in_sub_chapter",
        "title": "Header file1_in_sub_chapter",
    },
    {
        "location": "toplvl_chapter/sub_chapter/file1_in_sub_chapter/#header-file1_in_sub_chapter",
        "text": "text file1_in_sub_chapter",
        "title": "Header file1_in_sub_chapter",
    },
    {
        "location": "toplvl_chapter/sub_chapter/file2_in_sub_chapter/",
        "text": "Header file2_in_sub_chapter text file2_in_sub_chapter",
        "title": "Header file2_in_sub_chapter",
    },
    {
        "location": "toplvl_chapter/sub_chapter/file2_in_sub_chapter/#header-file2_in_sub_chapter",
        "text": "text file2_in_sub_chapter",
        "title": "Header file2_in_sub_chapter",
    },
    {
        "location": "toplvl_chapter/sub_chapter/unreferenced_in_sub_chapter/",
        "text": "Header unreferenced_in_sub_chapter text unreferenced_in_sub_chapter",
        "title": "Header unreferenced_in_sub_chapter",
    },
    {
        "location": "toplvl_chapter/sub_chapter/unreferenced_in_sub_chapter/#header-unreferenced_in_sub_chapter",
        "text": "text unreferenced_in_sub_chapter",
        "title": "Header unreferenced_in_sub_chapter",
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
