// 00_variable.js

// 1. let은 한번 선언하면 바꿀 수 없는 변수!
// 값의 변경은 가능
// 블록 유효범위를 갖는 지역변수 생성
// 블록 유효범위 : if / for / 함수에서 중괄호 내부
// 선언과 동시에 원하는 값으로 초기화
let x = 1
x = 2
// let x = 2 // already declared error

if (x === 2) {
    let x = 5
    console.log(x)
}

console.log(x)

// 2. const
// 재선언 + 값을 바꾸는 것이 불가
// 얘도 block scope
const MY_FAV = 7
console.log('my fav num is :'+MY_FAV)

if (MY_FAV===7) {
    const MY_FAV = 20
    console.log(MY_FAV)
}
console.log(MY_FAV)

// 3. var
// ES 6 이전에 쓰고, 현재 문제를 많이 발생시킴 : 절대 사용 X
// var로 선언된 변수의 범위는 현재 실행 문맥인데, 그 문맥이 함수 혹은 외부 전역으로도 갈 수 있음
// Hoisting (선언 끌어올리기) 같은 현상의 문제점 발생 요인

function varTest() {
    var x = 1
    if (true) {
        var x = 2
        console.log(x)
    }
    console.log(x)
}

function letTest() {
    let x = 1
    if (true) {
        let x = 2
        console.log(x)
    }
    console.log(x)
}

varTest()

letTest()

/* 
    정리
    1. var : 할당 및 선언 자유 : 함수 스코프
    2. let : 할당 자유, 선언은 한번만, 블록 스코프
    3. const : 할당 및 선언 한번만, 블록 스코프
*/

// 4. 식별자
// 변수명은 식별자라고 불리며, 특정 규칙을 따른다.
// 반드시 문자, 달러, 또는 밑줄로 시작해야 한다
// 대소문자를 구분하며 클래스명을 제외하고는 대문자로 시작 X

// 숫자, 문자, Boolean
let dog
let variableName

// 배열 - 복수형 이름을 사용
const dogs = []

// 함수
function getPropertyName() {
    ...
}

// Boolean 반환 함수 - 반환 값이 Boolean인 함수는 is로 시작
let isAvailable = false

// 클래스, 생성자 (파스칼 케이스 사용)
class User {
    constructor(options) {
        this.name = options.name
    }
}

const good = new User({
    name : 'kang',
})

// 상수 (대문자 스네이크 케이스)
export const API_KEY = 'SOMEKEY'