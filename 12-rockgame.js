let score=JSON.parse(localStorage.getItem('score')) || {
  wins:0,
  losses:0,
  ties:0
};

updateScoreElement();
/*
if(score === null){
  score={
    wins:0,
    losses:0,
    ties:0
  }
}*/
let isAutoPlaying= false;
let intervalID;

/*const autoPlay = () => {

}*/ 


function autoPlay(){

  if(!isAutoPlaying){
      intervalID=setInterval(() => {
      const playerMove=pickComputerMove();
      playGame(playerMove);
    },3000);
    isAutoPlaying=true;
    
  }else{
    clearInterval(intervalID);
    isAutoPlaying=false;
  }
  
}

document.querySelector('.js-rock-button')
  .addEventListener('click',()=>{
    playGame('rock');
  });

document.querySelector('.js-paper-button')
  .addEventListener('click',()=>{
    playGame('paper');
  });

document.querySelector('.js-scissors-button')
 .addEventListener('click', ()=>{
    playGame('scissors');
 });

 document.body.addEventListener('keydown',(event)=>{
  if(event.key === 'r'){
    playGame('rock');
  }else if(event.key === 'p'){
    playGame('paper');
  }else if(event.key === 's'){
    playGame('scissors');
  }
 });

function playGame(playerMove){
  const computerMove=pickComputerMove();

  let result='';

  if(playerMove==='scissors'){
        if(computerMove === 'Rock'){
        result='You Lose';
      }else if(computerMove === 'Paper'){
        result='You Win';
      }else if(computerMove==='scissors'){
        result='Tie';
      }
      
    }else if(playerMove==='Paper'){
      if(computerMove === 'Rock'){
      result='You Win';
    }else if(computerMove === 'Paper'){
      result='Tie';
    }else if(computerMove==='scissors'){
      result='You Lose';
    }
  }else if(playerMove='Rock'){
    if(computerMove === 'Rock'){
    result='Tie';
  }else if(computerMove === 'Paper'){
    result='You Lose';
  }else if(computerMove==='scissors'){
    result='You Win';
  }
  }

  if(result==='You Win'){
    score.wins++;
  }else if(result==='You Lose'){
    score.losses++;
  }else if( result==="Tie"){
    score.ties++;
  }

  localStorage.setItem('score',JSON.stringify(score));

  updateScoreElement();

  document.querySelector('.js-result')
    .innerHTML=result;

  document.querySelector('.js-moves')
  .innerHTML = `You <img class="image-game" src="${playerMove}-emoji.png"> <img class="image-game" src="${computerMove}-emoji.png">Computer`;

  alert(`You picked ${playerMove}. Computer picked ${computerMove}. ${result}
Wins:${score.wins}, Losses:${score.losses}, Ties:${score.ties} `);
}

function updateScoreElement(){
  document.querySelector('.js-score')
    .innerHTML = `Wins:${score.wins}, Losses:${score.losses}, Ties:${score.ties}`;
}
    
function pickComputerMove(){
  const randomNumber = Math.random();
  let computerMove = '';

  if(randomNumber>=0 && randomNumber<1/3){
    computerMove='Rock';
  }else if(randomNumber>=1/3 && randomNumber<2/3){
    computerMove='Paper';
  }else if(randomNumber>=2/3 && randomNumber<1){
    computerMove='scissors';
  }
  return computerMove;
}
