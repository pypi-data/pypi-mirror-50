# NGINX Content-Security-Policy header generator

[![Build Status](https://travis-ci.com/GianOrtiz/nginxcsp.svg?branch=master)](https://travis-ci.com/GianOrtiz/nginxcsp) [![Coverage Status](https://coveralls.io/repos/github/GianOrtiz/nginxcsp/badge.svg?branch=master)](https://coveralls.io/github/GianOrtiz/nginxcsp?branch=master)

This tool will generate `Content-Security-Policy` headers for a NGINX configuration file from import domains in HTML files.

## Usage

To generate `Content-Security-Policy` headers from HTML files in a path you can use the following command:

```
nginxcsp /path/to/html/files --out /path/to/nginx.conf --override
```

the command will generate `Content-Security-Policy`, `X-Content-Security-Policy` and `X-WebKit-CSP` headers for all `server` blocks of your `nginx.conf` file and remove the past ones. The headers will be generate from the tags in your html files, for example if you have an HTML file with the tag `<script src="https://cdnjs.cloudflare.com/some-script.js"></script>` you would get the header `Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdnjs.cloudfare.com; img-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; object-src 'self'"`.

If you would like to create only the `Content-Security-Policy` header you can use the flag `--csp`, the same applies for `X-Content-Security-Policy` with `--xcsp` and for `X-WebKit-CSP` with `--xwebkit`.

You can get all the usage help using `nginxcsp -h`:

```
usage: nginxcsp html_path

Search content loading sources in HTML files and Content-Security-Policy
headers automatically.

positional arguments:
  html_path             the path of the HTML files

optional arguments:
  -h, --help            show this help message and exit
  --out OUT             NGINX configuration file to output the generated
                        headers
  --server_name SERVER_NAME
                        the server_name in the NGINX server block to add CSP
                        headers
  --port PORT           the port from "listen {port}" line in a NGINX server
                        block to add CSP headers
  --override            flag to override the headers in the out file
  --csp                 flag to generate only the Content-Security-Policy
                        header
  --xcsp                flag to generate only the X-Content-Security-Policy
                        header
  --xwebkit             flag to generate only the X-WebKit-CSP header
```
