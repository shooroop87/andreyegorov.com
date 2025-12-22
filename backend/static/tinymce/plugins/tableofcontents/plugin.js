tinymce.PluginManager.add('tableofcontents', function(editor, url) {
  
  const generateTOC = () => {
    const content = editor.getContent();
    const temp = document.createElement('div');
    temp.innerHTML = content;
    
    const headings = temp.querySelectorAll('h2, h3');
    
    if (headings.length === 0) {
      editor.notificationManager.open({
        text: 'No headings found',
        type: 'warning'
      });
      return;
    }

    let tocHTML = '<div class="table-of-contents"><h2>Table of Contents</h2><ul>';
    let prevLevel = 0;
    
    headings.forEach((heading, index) => {
      const level = parseInt(heading.tagName.substring(1));
      const text = heading.textContent;
      const id = `toc-${index}`;
      
      heading.id = id;
      
      if (level > prevLevel) {
        tocHTML += '<ul>'.repeat(level - prevLevel);
      } else if (level < prevLevel) {
        tocHTML += '</ul>'.repeat(prevLevel - level);
      }
      
      tocHTML += `<li><a href="#${id}">${text}</a></li>`;
      prevLevel = level;
    });
tocHTML += '</ul>'.repeat(prevLevel) + '</ul></div>';
    
    editor.setContent(temp.innerHTML);
    editor.insertContent(tocHTML);
  };

  editor.ui.registry.addButton('tableofcontents', {
    text: 'TOC',
    icon: 'ordered-list',
    tooltip: 'Insert Table of Contents',
    onAction: generateTOC
  });

  editor.ui.registry.addMenuItem('tableofcontents', {
    text: 'Table of Contents',
    icon: 'ordered-list',
    onAction: generateTOC
  });

  return {
    getMetadata: () => ({
      name: 'Table of Contents',
      url: 'https://abroadstours.com'
    })
  };
});