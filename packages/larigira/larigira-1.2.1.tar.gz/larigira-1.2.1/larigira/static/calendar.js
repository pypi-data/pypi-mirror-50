/* global jQuery */
jQuery(function ($) {
  $('.button').button({
    icons: {
      primary: 'ui-icon-pencil'
    }
  })

  $('li.alarm').hover(function () {
    var sel = 'li.alarm[data-alarmid="' + $(this).data('alarmid') + '"]'
    $(sel).closest('div').find('time').toggleClass('soft-highlight')
  })
  $('li.alarm').click(function () {
    var alarmid = $(this).data('alarmid')
    var actions = $(this).data('actions')
    var content = $('<div/>').append(
      $('<p/>').append($('<a class="btn btn-default"/>').text('Modifica orario evento').attr('href', 'edit/time/' + alarmid))
    )
    if (Number.isInteger(actions)) { // else, it's a string representing a list
      content.append($('<p/>').append(
      $('<a class="btn btn-default"/>')
      .text('Modifica audio evento')
      .attr('href', 'edit/audio/' + actions)))
    }
    var audio = $('<p/>').append($('<a class="btn btn-default btn-sm"/>').text('Modifica lista di audio evento').attr('href', 'edit/event/' + alarmid))
    content.append(audio).dialog({modal: true, title: 'Evento ' + $(this).text()})
  })

  $(document).tooltip({
    items: 'li.alarm',
    content: function () {
      var el = $(this)
      return el.find('.alarm-actions').html()
    }
  })
})

