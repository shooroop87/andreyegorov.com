tinymce.PluginManager.add('accordion', function(editor, url) {
  
  const openDialog = function () {
    return editor.windowManager.open({
      title: 'Вставить аккордеон',
      body: {
        type: 'panel',
        items: [
          {
            type: 'input',
            name: 'title',
            label: 'Заголовок секции',
            placeholder: 'Введите заголовок'
          },
          {
            type: 'textarea',
            name: 'content',
            label: 'Содержимое',
            placeholder: 'Введите текст'
          }
        ]
      },
      buttons: [
        {
          type: 'cancel',
          text: 'Отмена'
        },
        {
          type: 'submit',
          text: 'Вставить',
          primary: true
        }
      ],
onSubmit: function (api) {
        const data = api.getData();
        
        const html = `
<div class="accordion -simple row y-gap-20 mt-30 js-accordion">
  <div class="col-12">
    <div class="accordion__item px-20 py-15 border-1 rounded-12">
      <div class="accordion__button d-flex items-center justify-between">
        <div class="button text-16 text-dark-1">${data.title || 'Заголовок'}</div>
        <div class="accordion__icon size-30 flex-center bg-light-2 rounded-full">
          <i class="icon-plus text-13"></i>
          <i class="icon-minus text-13"></i>
        </div>
      </div>
      <div class="accordion__content">
        <div class="pt-20 ck-content">
          <p class="mt-20">${data.content || 'Содержимое аккордеона'}</p>
        </div>
      </div>
    </div>
  </div>
</div>`;
        
        editor.insertContent(html);
        api.close();
      }
    });
  };
// Кнопка в тулбаре
  editor.ui.registry.addButton('accordion', {
    text: 'Аккордеон',
    icon: 'accordion',
    tooltip: 'Вставить аккордеон',
    onAction: function () {
      openDialog();
    }
  });

  // Пункт меню
  editor.ui.registry.addMenuItem('accordion', {
    text: 'Аккордеон',
    icon: 'accordion',
    onAction: function () {
      openDialog();
    }
  });

  return {
    getMetadata: function () {
      return {
        name: 'Accordion Plugin',
        url: 'https://example.com'
      };
    }
  };
});