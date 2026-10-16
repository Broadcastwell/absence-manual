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

test('manual reading controls retain accessible colors after shared tokens load',()=>{
 const manual=read('docs/assets/manual.css'),combined=manual+'\n'+read('docs/assets/site-chrome.css');
 const declaration=(selector,property)=>manual.split(selector+' {')[1].split('}')[0].match(new RegExp('(?:^|;)\\s*'+property+':([^;]+)'))[1].trim();
 const token=name=>[...combined.matchAll(new RegExp(name+':\\s*(#[a-fA-F0-9]{6})','g'))].at(-1)[1];
 const resolve=color=>color.startsWith('var(')?token(color.slice(4,-1)):color;
 const luminance=color=>color.slice(1).match(/../g).map(n=>parseInt(n,16)/255).map(n=>n<=.04045?n/12.92:((n+.055)/1.055)**2.4).reduce((sum,n,i)=>sum+n*[.2126,.7152,.0722][i],0);
 const contrast=(a,b)=>{const x=luminance(resolve(a)),y=luminance(resolve(b));return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
 const active=declaration('.md-nav__item .md-nav__link--active','color');
 assert(contrast(active,'#F7F9FC')>=4.5,'active chapter/TOC text');
 const buy=manual.split('.md-typeset a.bw-buy{')[1].split('}')[0];
 assert(contrast(buy.match(/(?:^|;)background:([^;]+)/)[1],'#FFFFFF')>=4.5,'white purchase label');
 const repository=declaration('.md-nav__source .md-source','color'),drawer=declaration('.md-nav__source','background-color');
 assert(contrast(repository,drawer)>=4.5,'phone drawer repository label');
 assert(contrast('#3B82F6','#FFFFFF')<4.5,'known failed prior button color is rejected');
 assert(contrast('#101828','#303FA1')<4.5,'known failed prior drawer pair is rejected');
});
