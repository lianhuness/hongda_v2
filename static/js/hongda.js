$(document).ready(function(){
   $("#today_date").text(function(){
       return new Date().toLocaleDateString();
   });
});