// 05_array_helper_method.js

// 1. forEach
// array.forEach(callback(element, index, array))
// ES6 +

const colors = ['red', 'blue', 'green']
colors.forEach(function(color) {
    console.log(color)
})

colors.forEach( color => console.log(color))

// 2. map
// array.map(callback(element))
// 배열 내의 모든 요소에 대해 각각 주어진 함수를 호출한 결과를
// 모아서 새로운 배열을 return

const numbers = [1,2,3]

const double_numbers = numbers.map(function(num){
    return num * 2
})

const double_numbers = numbers.map( num => num * 2)

// 3. filter
// array.filter(callback(element))
// 주어진 함수의 테스트(조건)를 통과하는 모든 요소를 모아 새로운 배열을 반환

const products = [
    { name : 'cucumber', type : 'vegetable' },
    { name : 'banana', type : 'fruit' },
    { name : 'apple', type : 'fruit'}
]

const fruit_product = products.filter(function(product){
    return product.type === 'fruit'
})
fruit_products // [{ name : 'cucumber', type : 'vegetable' }, { name : 'banana', type : 'fruit' }]