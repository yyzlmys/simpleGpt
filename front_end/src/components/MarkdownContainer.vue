<template>
    <div class="markdown-container" v-html="renderedMarkdown"></div>
  </template>
  
  <script>
  import MarkdownIt from 'markdown-it';
  import katex from 'markdown-it-katex';
  import hljs from 'highlight.js'
  import 'highlight.js/styles/default.css';
  import 'katex/dist/katex.min.css';

  export default {
    props: {
      markdownContent: {
        type: String,
        required: true
      }
    },
    computed: {
      renderedMarkdown() {

        const md = MarkdownIt({
        highlight: function (str, lang) {
          if (lang && hljs.getLanguage(lang)) {
            try {
              return hljs.highlight(str, { language: lang }).value;
            } catch (__) {}
          }

          return '';
        }
        });
        md.use(katex);
        return md.render(this.markdownContent);
      }
    }
  };
  </script>
  
  <style>
  

.markdown-container {
  max-width: 900px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  font-size: 16px;
}


.markdown-container h1 {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.markdown-container h2 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 16px;
}

.markdown-container h3 {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 12px;
}

.markdown-container h4 {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.markdown-container h5 {
  font-size: 14px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.markdown-container h6 {
  font-size: 12px;
  font-weight: bold;
  color: #333;
  margin-bottom: 6px;
}


.markdown-container p {
  margin-bottom: 16px;
}


.markdown-container ul,
.markdown-container ol {
  margin-bottom: 16px;
}

.markdown-container ul li {
  margin-bottom: 8px;
}

.markdown-container ol li {
  margin-bottom: 8px;
}


.markdown-container a {
  color: #007bff;
}

.markdown-container a:hover {
  color: #0056b3;
}


.markdown-container pre {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 5px;
  overflow: auto;
}

.markdown-container code {
  font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
}


.markdown-container blockquote {
  border-left: 4px solid #007bff;
  padding-left: 10px;
  margin-left: 0;
}


.markdown-container img {
  max-width: 100%;
  height: auto;
  margin-bottom: 16px;
}

  </style>
  