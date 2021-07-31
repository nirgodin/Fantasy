class WebController:

    def __init__(self):
        pass

    @staticmethod
    def _click_dropdown_menu(menu_button, category_name: str) -> None:
        menu_button.select_by_visible_text(category_name)

        return None
