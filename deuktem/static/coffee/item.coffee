views['item-list'] = ->
    $('#nav-item-list').addClass('active')


views['item-new'] = ->
    $('#nav-item-new').addClass('active')

    $('#item-new-file').change ->
        preview = $('#item-new-photo')
        if this.files && this.files[0]
            reader = new FileReader()
            reader.readAsDataURL(this.files[0])
            reader.onload = (e) ->
                preview.attr('src', e.target.result)
                preview.css('height', 'auto')

    $('#item-new-form').submit ->
        name = $('#item-new-name')
        description = $('#item-new-description')

        if not name.val()
            error("아이템 이름을 입력해주세요.")
            name.parent().addClass('has-error')
            name.focus()
            return false
        return true

    $('#item-new-name').on 'input', ->
        $(this).parent().removeClass('has-error')

    error = (msg) ->
        errorAlert = $('#item-new-error')
        errorAlert.text(msg)

        if errorAlert.hasClass('hidden')
            errorAlert.removeClass('hidden')
            delay = 1
        else
            errorAlert.removeClass('in')
            delay = 100

        setTimeout((-> errorAlert.addClass('in')), delay)
