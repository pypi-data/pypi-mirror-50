import os
from ..html_parser import RefParser


class HeaderGenerator():

    def generate_headers(self, path):
        content = self.generate_header_content(path)
        return {"Content-Security-Policy":
                self.generate_content_security_policy(content),
                "X-Content-Security-Policy":
                self.generate_x_content_security_policy(content),
                "X-WebKit-CSP":
                self.generate_x_webkit_csp(content)}

    def generate_content_security_policy(self, content):
        header = 'add_header Content-Security-Policy {0};'.format(content)
        return header

    def generate_x_content_security_policy(self, content):
        header = 'add_header X-Content-Security-Policy {0};'.format(content)
        return header

    def generate_x_webkit_csp(self, content):
        header = 'add_header X-WebKit-CSP {0};'.format(content)
        return header

    def generate_header_content(self, path):
        files = self.__get_files_from_path(path)
        ref_parser = RefParser()
        for file in files:
            data = open(file).read()
            ref_parser.feed(data)

        script_src = self.__get_script_src_from_list(ref_parser.script_src)
        img_src = self.__get_img_src_from_list(ref_parser.img_src)
        style_src = self.__get_style_src_from_list(ref_parser.link_href)
        default_src = self.__get_default_src_from_list()
        font_src = self.__get_font_src_from_list()
        object_src = self.__get_object_src_from_list()

        header_text = '"default-src {0}; script_src {1}; img_src {2}; ' + \
            'style_src {3}; font_src {4}; object_src {5}";'
        header = header_text.format(
            default_src, script_src, img_src, style_src, font_src, object_src)
        return header

    def __get_files_from_path(self, path):
        files = []
        if os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith(".html"):
                    files.append(os.path.join(path, filename))
        else:
            files = [path]
        return files

    def __remove_duplicate_references_from_list(self, list_):
        list_src = []
        for src in list_:
            if src["scheme"] == "":
                list_src.append(src["netloc"])
                list_.remove(src)
        for src in list_:
            if src["netloc"] not in list_src:
                list_src.append(src["scheme"]+"://"+src["netloc"])
                list_.remove(src)
        return list_src

    def __get_script_src_from_list(self, scripts):
        scripts = self.__remove_duplicate_references_from_list(
            scripts)
        script_src = "'self' 'unsafe-inline' 'unsafe-eval'"
        for script in scripts:
            script_src += " {0}".format(script)
        return script_src

    def __get_img_src_from_list(self, imgs):
        imgs = self.__remove_duplicate_references_from_list(
            imgs)
        img_src = "'self'"
        for img in imgs:
            img_src += " {0}".format(img)
        return img_src

    def __get_style_src_from_list(self, styles):
        styles = self.__remove_duplicate_references_from_list(
            styles)
        style_src = "'self' 'unsafe-inline'"
        for style in styles:
            style_src += " {0}".format(style)
        return style_src

    def __get_default_src_from_list(self):
        default_src = "'self'"
        return default_src

    def __get_font_src_from_list(self):
        font_src = "'self'"
        return font_src

    def __get_object_src_from_list(self):
        object_src = "'self'"
        return object_src
