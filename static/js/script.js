
backdrop = document.getElementById('myBackdrop');
register = document.getElementById('register');
registerPage = document.getElementById('registration');
closeBtns = document.querySelectorAll('.closeBtn');
signIn = document.getElementById('sign-in');
loginPage = document.getElementById('login');

register.addEventListener('click', () => {
    console.log('clicked!!')
    backdrop.classList.add('is-active');
    registerPage.classList.add('is-active');

});

signIn.addEventListener('click', () => {
    console.log('clicked!!')
    backdrop.classList.add('is-active');
    loginPage.classList.add('is-active');

});

backdrop.addEventListener('click', () =>{
    backdrop.classList.remove('is-active');
    registerPage.classList.remove('is-active');
    loginPage.classList.remove('is-active');
});


closeBtns.forEach(closeBtn => {
    closeBtn.addEventListener('click', () => {
        backdrop.classList.remove('is-active');
        registerPage.classList.remove('is-active');
        loginPage.classList.remove('is-active');
    });
});

