from ..app import Application
import argparse


class CLI():

    def __init__(self):
        self.setup()

    def setup(self):
        self.argument_parser = argparse.ArgumentParser(
            "CSP NGINX Generator", "nginxcsp html_path",
            "Search content loading sources in HTML files and "
            + "Content-Security-Policy headers automatically.")
        self.argument_parser.add_argument(
            "html_path", help="the path of the HTML files")
        self.argument_parser.add_argument(
            "--out", help="NGINX configuration file to output the generated "
            + "headers")
        self.argument_parser.add_argument(
            "--server_name", help="the server_name in the NGINX server block "
            + "to add CSP headers")
        self.argument_parser.add_argument(
            "--port", help="the port from \"listen {port}\" line in a NGINX "
            + "server block to add CSP headers")
        self.argument_parser.add_argument(
            "--override", help="flag to override the headers in the out file",
            action="store_true")
        self.argument_parser.add_argument(
            "--csp", help="flag to generate only the Content-Security-Policy "
            + "header", action="store_true")
        self.argument_parser.add_argument(
            "--xcsp", help="flag to generate only the X-Content-Security"
            + "-Policy header", action="store_true")
        self.argument_parser.add_argument(
            "--xwebkit", help="flag to generate only the X-WebKit-CSP header",
            action="store_true")
        self.args = self.argument_parser.parse_args()

    def run(self):
        app = Application(self)
        app.run()

    def get_html_path(self):
        return self.args.html_path

    def get_out_file(self):
        out_file = None
        if self.args.out:
            out_file = self.args.out
        return out_file

    def get_server_name(self):
        server_name = None
        if self.args.server_name:
            server_name = self.args.server_name
        return server_name

    def get_port(self):
        port = None
        if self.args.port:
            port = self.args.port
        return port

    def get_override(self):
        return self.args.override

    def get_csp(self):
        return self.args.csp

    def get_xcsp(self):
        return self.args.xcsp

    def get_xwebkit(self):
        return self.args.xwebkit
