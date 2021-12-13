/*
 FireShot - Webpage Screenshots and Annotations
 Copyright (C) 2007-2021 Evgeny Suslikov (evgeny@suslikov.ru)
*/
window.fsActivationEvents||(window.fsActivationEvents=!0,chrome.runtime.sendMessage({message:"checkFSAvailabilityEvt"},function(a){document.addEventListener("checkFSAvailabilityEvt",function(c){for(var b in a)a.hasOwnProperty(b)&&c.target.setAttribute(b,a[b])},!1)}),document.addEventListener("activateFireShotEvt",function(a){chrome.runtime.sendMessage({message:"activateFireShot",name:a.target.getAttribute("FSName"),key:a.target.getAttribute("FSKey")},function(c){})},!1));var element=document.createElement("FireShotDataElement");
document.documentElement.appendChild(element);var evt=document.createEvent("Events");evt.initEvent("helloFromFireShotForChrome",!0,!1);element.dispatchEvent(evt);document.documentElement.removeChild(element);
