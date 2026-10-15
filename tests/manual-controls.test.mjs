import {test} from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
const read=p=>fs.readFileSync(new URL('../'+p,import.meta.url),'utf8');
function simulate(){
 const document={activeElement:null};
 function node(){const handlers={};return {checked:false,attrs:{},handlers,addEventListener(n,fn){(handlers[n]||=[]).push(fn)},dispatchEvent(e){for(const fn of handlers[e.type]||[])fn(e)},setAttribute(n,v){this.attrs[n]=v},focus(){document.activeElement=this}}}
 const search=node(),query=node(),toggle=node(),button=node(),drawer=node(),chapter=node(),overlay=node(),back=node();
 button.dataset={manualToggle:'__search'};chapter.dataset={manualToggle:'__drawer'};
 overlay.classList={contains:()=>false};back.classList={contains:c=>c==='md-search__icon'};
 search.querySelector=()=>query;search.querySelectorAll=()=>[overlay,back];search.contains=n=>[query,back,overlay].includes(n);
 document.querySelector=s=>s==='[data-md-component="search"]'?search:button;
 document.querySelectorAll=()=>[button,chapter];document.getElementById=id=>id==='__search'?toggle:drawer;
 vm.runInNewContext(read('docs/assets/manual-controls.js'),{document,Event:class {constructor(type){this.type=type}}});
 const fire=(el,type='click',key)=>el.dispatchEvent({type,key,preventDefault(){}});
 return {document,search,query,toggle,button,drawer,chapter,overlay,back,fire};
}
test('manual search focuses its input and both touch dismissal targets restore the toolbar focus',()=>{
 const ui=simulate();
 for(const target of [ui.back,ui.overlay]){
  ui.fire(ui.button);assert.equal(ui.toggle.checked,true);assert.equal(ui.document.activeElement,ui.query);assert.equal(ui.button.attrs['aria-expanded'],'true');
  ui.fire(target);assert.equal(ui.toggle.checked,false);assert.equal(ui.document.activeElement,ui.button);assert.equal(ui.button.attrs['aria-expanded'],'false');
 }
 const css=read('docs/assets/site-chrome.css');
 assert.match(css,/\[data-md-toggle="search"\]:checked~\.bw-header \.md-search__overlay\[for="__search"\]\{display:block\}/);
 assert.match(css,/\[data-md-toggle="search"\]:checked~\.bw-header \.md-search__icon\[for="__search"\]\{display:flex;[^}]*min-height:44px/);
});
test('manual search closes by Escape and keyboard back action while chapter state remains separate',()=>{
 const ui=simulate();ui.fire(ui.chapter);assert.equal(ui.drawer.checked,true);assert.equal(ui.chapter.attrs['aria-expanded'],'true');
 ui.fire(ui.button);ui.fire(ui.search,'keydown','Escape');assert.equal(ui.toggle.checked,false);assert.equal(ui.document.activeElement,ui.button);assert.equal(ui.drawer.checked,true);
 ui.fire(ui.button);ui.fire(ui.back,'keydown','Enter');assert.equal(ui.toggle.checked,false);assert.equal(ui.back.attrs['aria-label'],'Close search');assert.equal(ui.back.attrs.tabindex,'0');
});
