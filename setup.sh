mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = 10000\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml
