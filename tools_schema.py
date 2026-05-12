SAVE_NOTE_TOOL = {
    "name": "save_note",
    "description": (
        "Lưu một note mới vào kho notes của user. "
        "Dùng khi user yêu cầu 'Lưu/ghi/note/jot/save' bất kỳ thông tin nào"
        "Trả về note id để tham chiếu sau."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": (
                "Nội dung text của note, viết tiếng việt giữ nguyên ý user."
                "Không thêm prefix kiểu 'Note:' hay timestamp."
                ),
            }
        },
        "required": ["content"],
    },
}

LIST_NOTES_TOOL = {
    "name": "list_notes",
    "description": (
        "Liệt kê tất cả notes đã lưu, sắp xếp mới nhất lên đầu. "
        "Dùng khi user hỏi 'có những note gì', 'list note', 'xem note', "
        "hoặc cần lấy danh sách trước khi tìm kiếm/tóm tắt."
    ),
    "input_schema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

SEARCH_NOTE_TOOL = {
    "name": "search_note",
    "description": (
        "Tìm các note chứa từ khoá. Trả về danh sách rút gọn. "
        "Dùng khi user yêu cầu 'tìm/search note có chữ X'."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "Từ khoá cần tìm (case-insensitive)",
            },
        },
        "required": ["keyword"],
    },
}

SUMMARIZE_NOTE_TOOL = {
    "name": "summarize_note",
    "description": (
        "Lấy nội dung 1 note theo id để LLM tóm tắt. "
        "Khác list_notes chỉ trả id+content rút gọn — tool này trả full text."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "id": {
                "type": "string",
                "description": "Note id, lấy từ list_notes hoặc search_note",
            },
        },
        "required": ["id"],
    },
}

ALL_TOOLS = [SAVE_NOTE_TOOL, LIST_NOTES_TOOL, SEARCH_NOTE_TOOL, SUMMARIZE_NOTE_TOOL]