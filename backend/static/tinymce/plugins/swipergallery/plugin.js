// backend/core/static/tinymce/plugins/swipergallery/plugin.js
(function() {
    'use strict';
    
    tinymce.PluginManager.add('swipergallery', function(editor, url) {
        
        // Хранилище для выбранных изображений
        var selectedImages = [];
        
        // Функция для открытия file picker
        function openFilePicker(callback) {
            editor.windowManager.open({
                title: 'Add Image to Gallery',
                body: {
                    type: 'panel',
                    items: [
                        {
                            type: 'input',
                            name: 'imageUrl',
                            label: 'Image URL (or click Browse)',
                        },
                        {
                            type: 'input',
                            name: 'altText',
                            label: 'Alt Text (optional)',
                        }
                    ]
                },
                buttons: [
                    {
                        type: 'custom',
                        name: 'browse',
                        text: 'Browse...',
                    },
                    { type: 'cancel', text: 'Cancel' },
                    { type: 'submit', text: 'Add Image', primary: true }
                ],
                onAction: function(api, details) {
                    if (details.name === 'browse') {
                        // Используем встроенный file picker TinyMCE
                        editor.windowManager.openUrl({
                            title: 'Select Image',
                            url: '/tinymce/upload/',
                            width: 800,
                            height: 600
                        });
                    }
                },
                onSubmit: function(api) {
                    var data = api.getData();
                    if (data.imageUrl.trim()) {
                        callback({
                            url: data.imageUrl.trim(),
                            alt: data.altText.trim() || 'Gallery image'
                        });
                    }
                    api.close();
                }
            });
        }
        
        // Главный диалог галереи
        function openGalleryDialog() {
            selectedImages = [];
            
            var dialogApi = editor.windowManager.open({
                title: 'Create Swiper Gallery',
                size: 'large',
                body: {
                    type: 'panel',
                    items: [
                        {
                            type: 'htmlpanel',
                            html: '<div style="margin-bottom:15px;padding:10px;background:#f5f5f5;border-radius:4px;">' +
                                  '<strong>Instructions:</strong> Enter image URLs below (one per line), or paste URLs from your media library.' +
                                  '</div>'
                        },
                        {
                            type: 'textarea',
                            name: 'imageUrls',
                            label: 'Image URLs (one per line)',
                            maximized: true,
                            minHeight: 250
                        },
                        {
                            type: 'selectbox',
                            name: 'galleryStyle',
                            label: 'Gallery Style',
                            items: [
                                { value: 'default', text: 'Default (with arrows & dots)' },
                                { value: 'minimal', text: 'Minimal (dots only)' },
                                { value: 'fullwidth', text: 'Full Width' },
                                { value: 'thumbs', text: 'With Thumbnails' }
                            ]
                        },
                        {
                            type: 'checkbox',
                            name: 'autoplay',
                            label: 'Autoplay'
                        },
                        {
                            type: 'checkbox',
                            name: 'loop',
                            label: 'Loop',
                        }
                    ]
                },
                initialData: {
                    imageUrls: '',
                    galleryStyle: 'default',
                    autoplay: false,
                    loop: true
                },
                buttons: [
                    { type: 'cancel', text: 'Cancel' },
                    { type: 'submit', text: 'Insert Gallery', primary: true }
                ],
                onSubmit: function(api) {
                    var data = api.getData();
                    var urls = data.imageUrls.split('\n').filter(function(url) {
                        return url.trim() !== '';
                    });
                    
                    if (urls.length === 0) {
                        editor.notificationManager.open({
                            text: 'Please enter at least one image URL',
                            type: 'error'
                        });
                        return;
                    }
                    
                    var html = generateGalleryHTML(urls, data);
                    editor.insertContent(html);
                    api.close();
                    
                    editor.notificationManager.open({
                        text: 'Gallery inserted! It will display as a slider on the live page.',
                        type: 'success',
                        timeout: 3000
                    });
                }
            });
        }
        
        // Генерация HTML для галереи
        function generateGalleryHTML(urls, options) {
            var galleryId = 'swiper-' + Date.now();
            var styleClass = 'swiper-gallery';
            
            // Добавляем класс стиля
            if (options.galleryStyle === 'fullwidth') {
                styleClass += ' swiper-gallery-fullwidth';
            } else if (options.galleryStyle === 'minimal') {
                styleClass += ' swiper-gallery-minimal';
            } else if (options.galleryStyle === 'thumbs') {
                styleClass += ' swiper-gallery-thumbs';
            }
            
            // Data-атрибуты для настроек
            var dataAttrs = 'data-swiper-id="' + galleryId + '"';
            dataAttrs += ' data-autoplay="' + (options.autoplay ? 'true' : 'false') + '"';
            dataAttrs += ' data-loop="' + (options.loop ? 'true' : 'false') + '"';
            dataAttrs += ' data-style="' + options.galleryStyle + '"';
            
            var html = '<div class="' + styleClass + '" ' + dataAttrs + '>';
            html += '<div class="swiper-wrapper">';
            
            urls.forEach(function(url, index) {
                var cleanUrl = url.trim();
                html += '<div class="swiper-slide">';
                html += '<img src="' + cleanUrl + '" alt="Gallery image ' + (index + 1) + '" loading="lazy">';
                html += '</div>';
            });
            
            html += '</div>';
            
            // Навигация в зависимости от стиля
            if (options.galleryStyle !== 'minimal') {
                html += '<div class="swiper-button-prev"></div>';
                html += '<div class="swiper-button-next"></div>';
            }
            
            html += '<div class="swiper-pagination"></div>';
            html += '</div>';
            
            // Добавляем thumbnails если выбран стиль с превью
            if (options.galleryStyle === 'thumbs') {
                html += '<div class="swiper-gallery-thumbs-container" data-swiper-thumbs="' + galleryId + '">';
                html += '<div class="swiper-wrapper">';
                urls.forEach(function(url, index) {
                    html += '<div class="swiper-slide">';
                    html += '<img src="' + url.trim() + '" alt="Thumb ' + (index + 1) + '">';
                    html += '</div>';
                });
                html += '</div>';
                html += '</div>';
            }
            
            return html;
        }
        
        // Регистрация кнопки
        editor.ui.registry.addButton('swipergallery', {
            text: 'Gallery',
            tooltip: 'Insert Swiper Gallery',
            icon: 'gallery',
            onAction: openGalleryDialog
        });
        
        // Регистрация пункта меню
        editor.ui.registry.addMenuItem('swipergallery', {
            text: 'Swiper Gallery',
            icon: 'gallery',
            onAction: openGalleryDialog
        });
        
        return {
            getMetadata: function() {
                return {
                    name: 'Swiper Gallery Plugin',
                    url: 'https://swiperjs.com'
                };
            }
        };
    });
})();