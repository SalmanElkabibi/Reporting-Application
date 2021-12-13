/*
 FireShot - Webpage Screenshots and Annotations
 Copyright (C) 2007-2021 Evgeny Suslikov (evgeny@suslikov.ru)
*/
function downloadInstaller(){fetch(chrome.extension.getURL("native/fireshot-chrome-plugin.dat")).then(function(b){return b.blob()}).then(function(b){var a=document.createElement("a");a.download="fireshot-chrome-plugin.exe";a.href=window.URL.createObjectURL(b);a.textContent="";a.dataset.downloadurl=["application/octet-stream",a.download,a.href].join(":");document.documentElement.appendChild(a);a.click();document.documentElement.removeChild(a)})}
document.addEventListener("DOMContentLoaded",function(){function b(){a.fsNativePlugin.ready?(gaTrack("UA-1025658-9","fireshot.com","NativeHostInstalled"),a.updateContextMenu(),a.doTrial(),window.close()):(getConsolePtr()("check"),a.fsNativePlugin.autoReconnect||a.fsNativePlugin.updating||a.fsNativePlugin.portBusy||(getConsolePtr()("connecting from page"),a.fsNativePlugin.init()),setTimeout(function(){b()},1E3))}var a=chrome.extension.getBackgroundPage();downloadInstaller();isOpera()?($("#img-step1-opera").toggle(),
$("#download-image").addClass("opera-download")):($("#img-step1").toggle(),$("#download-image").addClass("chrome-download"));b()});
