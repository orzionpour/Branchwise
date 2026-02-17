from branchwise.utils.diff_parser import DiffParser

def test_parse_simple_diff():
    patch = """@@ -1,2 +1,2 @@
-foo
+bar
"""
    changes = DiffParser.parse(patch)
    assert len(changes) == 1
    hunk = changes[0]
    assert hunk.old_line_start == 1
    assert hunk.new_line_start == 1
    assert len(hunk.lines) == 2
    assert hunk.lines[0] == ("-foo", None)
    assert hunk.lines[1] == ("+bar", 1)

def test_parse_diff_with_context():
    patch = """@@ -10,4 +10,4 @@
 def foo():
-    return 1
+    return 2
     pass
"""
    changes = DiffParser.parse(patch)
    assert len(changes) == 1
    hunk = changes[0]
    assert hunk.new_line_start == 10
    
    # Line 1: context " def foo():" -> line 10
    assert hunk.lines[0] == (" def foo():", 10)
    # Line 2: removed "-    return 1" -> None
    assert hunk.lines[1] == ("-    return 1", None)
    # Line 3: added "+    return 2" -> line 11
    assert hunk.lines[2] == ("+    return 2", 11)
    # Line 4: context "     pass" -> line 12
    assert hunk.lines[3] == ("     pass", 12)

def test_multiple_hunks():
    patch = """@@ -1,2 +1,2 @@
-foo
+bar
@@ -10,2 +10,2 @@
-baz
+qux
"""
    changes = DiffParser.parse(patch)
    assert len(changes) == 2
    assert changes[0].new_line_start == 1
    assert changes[1].new_line_start == 10
