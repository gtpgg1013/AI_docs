// 2. 객체(오브젝트)

const me = {
    name : 'DongWook',
    'phone number' : '01011111111',
    appleProducts: {
        ipad: '2018pro',
        iphone: '7+',
        macbook: '2019pro',
    }
}

me.name
me['name']

// 2 : ES6+

let books = ['Learnig JS', 'E JS']
let comics = {
    'DC' : ['Superman', 'Joker'],
    'Marvel' : ['Captain M', 'Avengers'],
}

let magazines = null

let bookshop = {
    books,
    comics,
    magazines,
}

// 3. JSON 
// object => String
const jsonData = JSON.stringify({
    coffee: 'Americano',
    iceCream: 'mint choco',
})

// String => object
const parsedData = JSON.parse(jsonData)