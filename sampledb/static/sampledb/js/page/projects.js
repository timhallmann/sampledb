import {
  updateTranslationJSON,
  setTranslationHandler,
  updateTranslationLanguages
} from "../sampledb-internationalization.js";

$(function (){
  window.translations = [];

  window.languages = window.template_values.language_info.languages;
  updateTranslationJSON();

  $('.select-language').selectpicker('val', ['' + window.template_values.language_info.english_id])

  $('#select-language-name').on('change', function () {
    updateTranslationLanguages(this, 'name-template', 'input-name-', ['name', 'description']);
  }).change();

  $('#select-language-description').on('change', function () {
    updateTranslationLanguages(this, 'description-template', 'input-description-', ['name', 'description']);
  }).change();

  $('.form-group[data-name="input-names"] [data-language-id], .form-group[data-name="input-descriptions"] [data-language-id]').each(function () {
    setTranslationHandler(this);
  });

  $('form').on('submit', function() {
    $('input').change();
    $('textarea').change();
    window.translations = $.map(window.translations, function(translation, index){
      if (translation.name  === '' && translation.description === '' && translation.language_id !== window.template_values.language_info.english_id){
        return null;
      }
      return translation;
    });
    updateTranslationJSON();
    return $(this).find('.has-error').length === 0;
  });
  if (window.template_values.language_info.show_create_form) {
    const create_modal = $('#createProjectModal');
    create_modal.removeClass('fade');
    create_modal.modal('show');
    create_modal.addClass('fade');
  }
});