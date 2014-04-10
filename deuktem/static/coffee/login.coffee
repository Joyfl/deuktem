views['login'] = ->
    $.getScript('//connect.facebook.net/en_US/all.js', ->
        window.fbAsyncInit = ->
            FB.init(appId: '419278264854168')
    )

    $('#login-fb').click ->
        $('#login-fb').button("loading")
        FB.getLoginStatus(facebookStatusCallback)

    facebookStatusCallback = (response) ->
        if response.status == 'connected'
            accessToken = response.authResponse.accessToken
            FB.api('/me?field=name', (response) ->
                $('#login-facebook-id').val(response.id)
                $('#login-facebook-token').val(accessToken)
                $('#login-form').submit()
            )
        else
            FB.login(facebookStatusCallback, scope: 'name')
