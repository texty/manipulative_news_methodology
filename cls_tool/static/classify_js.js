// Disable all links in fulltext

String.prototype.trunc = function(n){
    return (this.length > n) ? this.substr(0, n-1) + '...' : this;
};

// Buttons-checkbox
$('div.faketype input').change(function() {

   $(this).closest('label')
       .toggleClass('btn-dark')
       .toggleClass('btn-outline-dark');

});

$("#article_text *").each(function(i) { $(this).removeAttr('class').removeAttr('id').removeAttr('style'); });

// Keyboard checking
const keycodes = {
    '49': {'faketype': '1'},
    '50': {'faketype': '2'},
    '51': {'faketype': '3'},
    '52': {'faketype': '4'},
    '53': {'faketype': '5'},
    '54': {'faketype': '6'},
    '55': {'faketype': '7'},
    '56': {'faketype': '8'},
    '97': {'faketype': '1'},
    '98': {'faketype': '2'},
    '99': {'faketype': '3'},
    '100': {'faketype': '4'},
    '101': {'faketype': '5'},
    '102': {'faketype': '6'},
    '103': {'faketype': '7'},
    '104': {'faketype': '8'}
};

var keys = {};

$('body').keydown(function (e) {
    if ( document.URL.indexOf('classifier') > -1 &&
    e.which !== 40 && e.which !== 38 &&
    e.which !== 33 && e.which !== 34 &&
    e.which !== 35 && e.which !== 36 &&
    e.which !== 17 && e.which !== 70 &&
    (!$('#feedback_modal').is(':visible')) ) {
        e.preventDefault();
        var keycode = e.which;
        keys[keycode] = true;
        if ( keys[16] && keys[37] ) {
            $('.fa-clock-o').click();
        }

        if ( keys[16] && keys[39] ) {
            $('.fa-angle-right.fa-3x').click();
        }

        var keypressed = keycode.toString();

        if ( keycodes[keypressed] ) {
            if ( keys[16] ) {
                $('#id_types_' + keycodes[keypressed].faketype)
                .closest('label')
                .contextmenu();
            } else {
                $('#id_types_' + keycodes[keypressed].faketype)
                .closest('label')
                .click();
            }
        }

        if ( keycode === 13 ) {
            if ( $('#explanation_modal').is(':visible') ) {
                $('button[data-dismiss="modal"]').click();

            } else if ( $('#ner_tagger').is(':visible') ) {
                $('#submit_ner').click();

            } else {
                $('#submit_form').click();
            }
        }

        if ( $('#ner_tagger').is(':visible') ) {
            if ( keys[16] ) {
                if ( keys[80] ) {
                    $('input[value="P"]')
                        .parent()
                        .click();
                    $('#submit_ner').click();
                }
                if ( keys[76] ) {
                    $('input[value="L"]')
                        .parent()
                        .click();
                    $('#submit_ner').click();
                }
                if ( keys[79] ) {
                    $('input[value="O"]')
                        .parent()
                        .click();
                    $('#submit_ner').click();
                }
                if ( keys[68] ) {
                $('input[value="none"]')
                        .parent()
                        .click();
                    $('#submit_ner').click();
                }
            }
        }
    }
});

$('body').keyup(function (e) {
    if ( document.URL.indexOf('classifier') > -1 && e.which !== 40 && e.which !== 38 ) {
        e.preventDefault();
        delete keys[e.which];
    }
});

$(document).ready(function() {

    $('#article_text img').remove();

    var $links = $('#article_text a:not([data-toggle="popover"])');

    $links.each(function () {
        var $this = $(this);
        if ( $this.attr('href') ) {
            $this.attr('target', '')
            .attr('data-toggle', 'popover')
            .attr('data-trigger', 'focus')
            .attr('data-placement', 'top')
            .attr('title', 'Перейти за лінком')
            .attr('data-content',
                '<a href="' +
                $this.attr('href') +
                '" target="_blank" class="link">'+
                $this.attr('href').trunc(50) +
                '</a>')
            .attr('data-html', 'true')
            .attr('href', '#')
            .click(function (e) {
                e.preventDefault();
            })
            .popover();

        } else {
            $this.contents().unwrap();
        }
    });

    var explanations = $('#form-div').data('explanations').split(';;');
    $('.modal_button').contextmenu(function(e) {
        e.preventDefault();
        var targetModal = $(this).data('target');
        var buttonIndex = + $(this).find('input').attr('value') - 1;
        $('#explanation_modal_label').text( $(e.currentTarget).data('title') );
        $('#explanation_modal_description').text( explanations[buttonIndex] );
        $(targetModal).modal("show");

    });

    $('#feedback_button').click(function (e) {
        $( $(this).data('target') ).modal("show");
    });

    $('#options form').submit(function (e) {
        if ( $(e.target).find('div.faketype .btn-dark').length < 1 ) {
            e.preventDefault();
        }
    });

});
