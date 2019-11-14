// 02_type_operator.js

// Primitive 타입
// 1. Numbers
// const a = 13
// const b = -5
// const c = 3.14 // float
const d = 2.998e8
const e = Infinity
const f = -Infinity
const g = NaN // Not a number

// 2. String
const sentence1 = 'Ask and go to the blue' // single quote
const sentence2 = "Ask and go to the blue" // double quote
const sentence3 = `Ask and go to the blue` // backtick : python의 fstring 느낌?

// 2-2. 리터럴
const word2 = `안녕
하세요`
console.log(word2)

const age = 10
const message = `홍길동은 ${age}`
console.log(message)

const hacking = 'Happy' + 'Hacking' + '!'
console.log(hacking)

// 3. Boolean
true
false

// 4. Empty Value
let first_name
console.log(first_name) // undefined : 자동 할당

let last_name = null
console.log(last_name) // null : 의도적

typeof null // object : 설계 실수
typeof undefined // undefined

// 연산자
// 1. 할당 연산자
let c = 0

c += 10
console.log(c)

c -= 3
console.log(c)

c *= 10
console.log(c)

c++
console.log(c)

c--
console.log(c)

// 2. 비교 연산자
// 변수 앞에 var, const, let 안붙이면 자동으로 var 붙여줌
console.log(3 > 2) // true
3 < 2 // false

'A' < 'B' // true
'Z' < 'a' // true
'가' < '나' // true

// 3. 동등 연산자 : 동등 연산자의 사용은 '지양'한다
const a = 1
const b = '1'
console.log(a == b)
console.log(a != b)

// 4. 일치 연산자
console.log(a === b) // false
console.log(a === Number(b)) // true

// 5. 논리 연산자 (and / or / not)
true && false // false
true && true // true
1 && 0 // 0
0 && 1 // 0
console.log(4 && 7) // 7

// || : or는 그대로 : 앞에 있는게!

// 7. 삼항연산자
true ? 1 : 2 // 1

// 조건문과 반복문
// 1. if문
const userName = prompt("Hello/! Who are you?") // python의 input과 같은 느낌

let message = ''

if (userName === '1q2w3e4r') {
    message = "<h1>This is Secret Admin Page</h1>"
} else if (userName === 'Kang') {
    message = "<h1>Hello, Kang!</h1>"
} else {
    message = `<h1>Hello, ${userName}</h1>`
}

console.log(message)

// 2. switch문
const userName = prompt("Hello, who are you?")

let message = ''

switch(userName) {
    case '1q2w3e4r': {
        message = "secret"
        break
    }
    case 'Kang' : {
        message = "Hi kang"
        break
    }
    default: {
        message =  `hello, ${userName}`
    }
}

// 반복문
// 1. while loop
let i = 0

while (i < 6){
    console.log(i)
    i++
}

// 2. for loop
for (let j = 0; j < 6; j++){
    console.log(j)
}

const numbers = [0,1,2,3,4,5]

for (let number of numbers) {
    console.log(number)
}