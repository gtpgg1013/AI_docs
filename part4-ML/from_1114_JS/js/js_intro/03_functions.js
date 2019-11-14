// 03_functions.js

// 1. 선언식 (statement, declaration)
// 코드가 실행되기 전에 로드됨
function add(num1, num2) {
    return num1 + num2
}

console.log(add(2,2))

// 2. 표현식 (expression)
// 인터프리터가 해당 코드에 도달했을 때 로드
const sub = function(num1, num2) {
    return num1 - num2
}

// 3. Arrow Function
const greeting = function(name) {
    return `Hello! ${name}`
}

// 3-1. function 키워드 삭제
const greeting = (name) => { return `Hello ${name}`}

// 3-2. () 생략 (매개변수 1개)
const greeting = name => { return `Hello ${name}`}

// 3-3. {} & return 생략 (바디에 표현식이 1일경우)
const greeting = name => `Hello ${name}`

// 4. Anonymous Function (익명 함수)
(function (num) { return num ** 3 })(2)