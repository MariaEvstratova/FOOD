var doc = document.getElementById("script")
var name = doc.dataset.src
var myButton = document.getElementById(name)
var myModal = document.getElementById(name + '0')

console.log(myModal)
console.log(myButton)

myButton.addEventListener('click', () => {
    myModal.style.display = 'block';
    console.log('click')
    myModal.style.opacity = '1'
})
