import streamlit as st


class MultiPage:

    def __init__(self):
        self.pages = []

    def add_page(self, title, func):
        self.pages.append(
            {
                'title': title,
                'function': func
            }
        )

    def run(self):

        page = st.sidebar.selectbox(
            '功能選單',
            self.pages,
            format_func=lambda x: x['title']
        )

        page['function']()



if __name__ == '__main__':
    app = MultiPage()
    app.add_page('Shit', 'Hi')
    app.run()

