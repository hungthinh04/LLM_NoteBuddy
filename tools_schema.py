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

ALL_TOOLS = [SAVE_NOTE_TOOL,LIST_NOTES_TOOL]