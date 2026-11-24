from pathlib import Path
import json,base64
p=Path('index.html')
s=p.read_text(encoding='utf-8-sig')
Path('index.previous.html').write_text(s,encoding='utf-8')
s=s.replace('</style>', '''
canvas{background:#071c2d;cursor:grab}.globe-tools{display:flex;justify-content:space-between;align-items:center;gap:8px;margin:10px 0}.globe-tools button{padding:6px 12px;font-size:14px}.source{font-size:13px;color:#587064}.source a{color:#24694f}.choice-meta{display:grid;gap:5px;margin-top:12px;padding-top:10px;border-top:1px solid #dbe8df;font-size:14px}.choice-meta span{display:block}.choice-meta b{display:inline-block;min-width:48px;color:#255f48}.cost-note{font-size:14px;margin:12px 0;color:#5e7469}.cards{grid-template-columns:1fr}.cards details{padding:14px 16px}.cards p{font-size:15px;line-height:1.85}.choice-summary{background:#f0f6f2;padding:12px;border-radius:10px;font-size:14px;margin:12px 0}
</style>''')
s=s.replace('지도는 간략화한 그림입니다.', '위아래로도 회전할 수 있어요. 파란 바다와 실제 해안선을 관찰해 보세요.')
s=s.replace('<div class="buttons" id="countries">','<div class="globe-tools"><button id="grid-toggle" aria-pressed="false">위·경도선 보기</button><button id="home-globe">정면으로 보기</button></div><p class="source">지구 표면: Blue Marble 이미지 · <a href="https://science.nasa.gov/earth/earth-observatory/blue-marble-next-generation/" target="_blank" rel="noopener">NASA 자료 소개</a> · <a href="https://github.com/vasturiano/three-globe/blob/master/example/img/earth-blue-marble.jpg" target="_blank" rel="noopener">사용한 이미지</a></p><div class="buttons" id="countries">')
s=s.replace('<div id="choices" class="choices">','<p id="cost-note" class="cost-note" hidden>비용·시간·노력은 선택 비교를 위한 가상 예산입니다. 모든 나라에 동일한 원화 기준을 적용하며, 실제 견적이나 오존층 회복 기간이 아닙니다.</p><div id="choices" class="choices">')
s=s.replace('<div id="metrics" class="metrics">','<div id="choice-summary" class="choice-summary"></div><div id="metrics" class="metrics">')
s=s.replace('모든 수치와 역할의 자원은 임의로 만든 교육용 설정입니다.', '모든 효과 수치, 비용, 소요 시간과 역할의 자원은 임의로 만든 교육용 설정입니다. 노력은 개인의 실천 또는 조직의 협의·운영 부담을 뜻합니다.')
info=[
['한반도 남쪽에 있으며 동쪽에는 태백산맥, 서쪽에는 비교적 넓은 평야가 있어요. 여름은 덥고 습하고 겨울은 추워, 계절에 따라 냉방과 난방 사용이 달라져요.','수도는 서울이에요. 수도권의 도시 생활과 함께 반도체·자동차·조선 같은 제조업을 살펴볼 수 있어요. 가정의 전력 사용과 공장의 에너지 효율을 함께 생각해 보세요.','설날과 추석에는 가족이 모이고, 한글과 한복 같은 문화유산이 있어요. 전통문화뿐 아니라 영화·음악 등 현대 문화도 다양하게 발달해 있어요.','밥과 국, 여러 반찬을 함께 먹는 식사가 익숙해요. 김치와 장류 같은 발효 음식이 있으며, 지역별로 음식이 달라요. 냉장 보관과 음식물 낭비를 함께 생각해 보세요.'],
['동쪽에는 평야와 큰 강이, 서쪽에는 티베트고원과 사막이 있어요. 양쯔강과 황허 유역을 비롯해 지역마다 기후가 달라, 한 가지 환경으로 설명하기 어려워요.','수도는 베이징이며 상하이는 대표적인 해안 대도시예요. 공업 지대와 농촌이 함께 있어요. 공장 설비 개선과 지역별 에너지 수요를 함께 고려해 보세요.','춘절에는 가족이 모이고 지역별 축제와 전통 예술이 있어요. 넓은 국토에 여러 민족과 언어가 공존하며, 도시와 지역마다 생활 모습이 달라요.','북쪽에서는 밀을 이용한 면·만두를, 남쪽에서는 쌀밥을 자주 접할 수 있어요. 쓰촨 요리, 광둥 요리 등 지역별 조리법과 재료가 다양해요.'],
['북쪽에는 히말라야산맥, 중부와 남부에는 데칸고원이 있어요. 많은 지역에서 계절풍에 따른 우기와 건기가 나타나며, 더운 시기의 냉방과 물 사용을 생각해 볼 수 있어요.','수도는 뉴델리예요. 농업뿐 아니라 정보기술 산업과 제조업을 함께 살펴볼 수 있어요. 대도시와 농촌의 교통·전력 이용 여건이 다르다는 점을 고려해 보세요.','힌디어를 비롯해 여러 언어가 사용되며 다양한 종교가 공존해요. 디왈리와 홀리 같은 축제가 있지만 모든 사람이 같은 전통을 따르는 것은 아니에요.','쌀, 로티 같은 빵, 콩 요리 달과 여러 향신료를 활용해요. 채식을 하는 사람들도 있고 육류를 먹는 사람들도 있으며, 종교와 지역에 따라 음식이 달라요.'],
['스칸디나비아반도 서쪽에 있으며 빙하가 만든 깊은 만인 피오르가 있어요. 북부의 높은 위도 지역에서는 계절에 따라 낮과 밤의 길이 차이가 크게 나타나요.','수도는 오슬로예요. 수력 발전, 수산업, 해양 산업을 살펴볼 수 있으며 석유·가스 산업도 있어요. 추운 계절의 난방과 산업의 에너지 이용을 함께 생각해 보세요.','자연 속 산책·스키 등 야외 활동을 즐기는 문화가 있어요. 북부를 포함한 지역에는 사미인의 언어와 문화도 이어지고 있어요.','연어와 대구 등 생선, 감자, 빵을 활용한 음식이 있어요. 건조하거나 소금에 절이는 보존 방식도 있으며, 현대의 식생활은 지역과 가정마다 다양해요.'],
['서쪽에는 로키산맥, 가운데에는 넓은 평야, 동쪽에는 애팔래치아산맥이 있어요. 알래스카와 하와이를 포함하면 한랭 지역부터 열대 지역까지 자연환경이 다양해요.','수도는 워싱턴 D.C.예요. 금융·기술·농업·제조업 등 산업이 다양하고, 도시 간 거리가 먼 곳도 있어요. 이동 방식과 건물의 냉난방 효율을 함께 생각해 보세요.','여러 이주 배경과 원주민 공동체의 문화가 공존해요. 재즈·영화·야구 같은 문화 활동이 있으며 지역마다 생활 방식과 전통이 달라요.','햄버거뿐 아니라 바비큐, 남부 음식, 여러 이주 문화의 요리를 만날 수 있어요. 식재료를 장거리 운송하거나 냉장 보관할 때 필요한 에너지도 생각해 보세요.'],
['태평양과 안데스산맥 사이로 남북으로 길게 뻗어 있어요. 북쪽의 아타카마사막, 중부의 비교적 온화한 지역, 남쪽의 파타고니아와 빙하가 대비돼요.','수도는 산티아고예요. 구리 광업, 농업, 어업을 주제로 살펴볼 수 있어요. 광산과 도시의 전력 수요, 먼 지역까지 설비를 운송하는 조건을 함께 고려해 보세요.','스페인어가 널리 사용되며 마푸체 등 원주민의 문화도 이어져요. 쿠에카 같은 전통 춤과 지역별 축제, 다양한 문학·예술이 있어요.','엠파나다, 옥수수를 활용한 파스텔 데 초클로, 다양한 해산물 요리가 있어요. 해안과 내륙, 남북 지역에 따라 접할 수 있는 재료가 달라요.'],
['동아프리카 적도 부근에 있으며 해안 저지대, 고원, 케냐산, 대지구대가 있어요. 사바나뿐 아니라 숲과 산지도 있고, 고도에 따라 기온과 강수 조건이 달라요.','수도는 나이로비예요. 차와 커피 재배, 관광, 도시의 서비스업 등을 살펴볼 수 있어요. 도시와 농촌의 이동 거리, 전력과 냉장 설비 이용을 고려해 보세요.','스와힐리어와 영어가 공용어이며 여러 공동체의 언어와 전통이 있어요. 해안의 스와힐리 문화 등 다양한 문화를 하나로 단정하지 않고 살펴보세요.','옥수수가루로 만든 우갈리, 잎채소 요리 수쿠마 위키, 고기구이 냐마 초마 등이 있어요. 해안에서는 생선과 코코넛을 활용한 요리도 만날 수 있어요.'],
['남반구에 있어 한국과 계절이 반대예요. 내륙에는 건조한 지역이 넓고 북부는 열대 기후, 남동부는 비교적 온화한 기후가 나타나요. 북동쪽 바다에는 그레이트배리어리프가 있어요.','수도는 캔버라이며 시드니와 멜버른은 대표적인 대도시예요. 해안 도시의 생활, 광업·농축산업과 에너지 이용을 함께 살펴보세요. 넓은 국토의 이동 거리와 더운 날의 냉방 수요를 고려할 수 있어요.','애버리지널과 토레스해협 제도민은 서로 다른 여러 공동체와 문화를 이루고 있어요. 다양한 이주 문화도 공존해요. 야외 활동 때는 자외선 차단을 생각하되, 피부 보호와 오존층 보호 행동의 차이도 구분해 보세요.','해산물, 바비큐와 여러 이주 문화의 음식을 만날 수 있어요. 밀·쇠고기·유제품 등 다양한 식재료를 활용해요. 장거리 식품 운송과 냉장·냉동 설비의 에너지 및 냉매 관리를 함께 생각해 보세요.']
]
# 기존 나라의 위치와 상황을 유지하면서 소개문만 확장합니다.
start=s.index('const countries=[')
end=s.index('// 행동:',start)
old=s[start:end]
import re
names=re.findall(r"name:'([^']+)'",old)
coords=re.findall(r"lat:([-\d]+),lon:([-\d]+)",old)
contexts=re.findall(r"context:'([^']+)'",old)
data=[dict(name=n,lat=int(c[0]),lon=int(c[1]),info=i,context=t) for n,c,i,t in zip(names,coords,info,contexts)]
s=s[:start]+'const countries='+json.dumps(data,ensure_ascii=False,indent=2)+';\n'+s[end:]
insert='''
// 비용과 시간은 실제 견적이 아닌 수업용 비교 설정입니다.
const actionResources=[
 [
  {cost:'0~5만 원',time:'예약 대기 1~3일 · 실제 작업 약 1시간',effort:'낮음 · 수거처 확인, 예약, 수거 공간 정리'},
  {cost:'추가 지출 0원으로 가정',time:'하루 약 10~20분 · 1개월 이상 꾸준히',effort:'보통 · 대기전력 차단, 이동 경로와 생활 습관 조정'},
  {cost:'추가 비용 0원',time:'추가 시간 없음',effort:'추가 노력 없음 · 새로운 환경 실천은 하지 않음'}
 ],
 [
  {cost:'초기 8,000만 원 · 연간 운영 1,000만 원',time:'도입 2~3개월 · 이후 월 1회 점검',effort:'보통 · 기술자 점검, 회수업체 계약, 직원 교육'},
  {cost:'초기 개발·설비 투자 2억 원',time:'개발·시험 6~12개월',effort:'높음 · 설계 변경, 성능 검증, 생산 라인 조정'},
  {cost:'추가 투자 0원 · 기존 운영비는 별도',time:'추가 준비 시간 없음',effort:'추가 개선 노력 없음 · 기존 설비 운영은 지속'}
 ],
 [
  {cost:'시범 사업 총 30억 원',time:'제도 준비 6개월 · 시범 운영 1년',effort:'높음 · 규칙 마련, 회수 거점 설치, 담당자 교육'},
  {cost:'시범 사업 총 60억 원',time:'계획·협의 1년 · 단계적 도입 2~3년',effort:'매우 높음 · 주민 협의, 시설 심사, 지원 제도 운영'},
  {cost:'추가 편성 0원 · 기존 예산은 별도',time:'추가 정책 준비 시간 없음',effort:'추가 개선 노력 없음 · 기존 정책 집행은 지속'}
 ]
];
roles.forEach((r,i)=>r.choices.forEach((c,j)=>c.push(actionResources[i][j])));
function resourceText(c){const r=c[5];return '비용 '+r.cost+' / 시간 '+r.time+' / 노력 '+r.effort;}
'''
s=s.replace("const $=id=>",insert+"\nconst $=id=>")
s=s.replace('angle=120,effect=null,timer=null','angle=120,effect=null,timer=null,tilt=12')
s=s.replace('angle=selected.lon;resetResult()',"angle=selected.lon;tilt=Math.max(-45,Math.min(45,selected.lat*.6));$('cost-note').hidden=true;resetResult()")
a=s.index('function showChoices()')
b=s.index('function metric(',a)
s=s[:a]+'''function showChoices(){
 resetResult();$('choices').replaceChildren();$('cost-note').hidden=false;
 role.choices.forEach(c=>{
  const button=document.createElement('button'),description=document.createElement('small'),meta=document.createElement('div');
  button.textContent=c[0];description.textContent=c[1];meta.className='choice-meta';
  [['비용',c[5].cost],['시간',c[5].time],['노력',c[5].effort]].forEach(([label,value])=>{
   const line=document.createElement('span'),name=document.createElement('b');name.textContent=label;line.append(name,document.createTextNode(value));meta.append(line);
  });
  button.append(description,meta);button.onclick=()=>choose(c);$('choices').append(button);
 });
}
'''+s[b:]
s=s.replace("$('metrics').innerHTML=metric(","$('choice-summary').textContent='선택한 행동의 가상 자원: '+resourceText(c);$('metrics').innerHTML=metric(")
s=s.replace("+' — 오존층 상태 '","+' — '+resourceText(c)+' — 오존층 상태 '")
a=s.index("const canvas=$('globe')")
s=s[:a]+'''// 구체 표면의 각 픽셀에 실제 세계 지도를 투영합니다. 외부 라이브러리는 없습니다.
const canvas=$('globe'),ctx=canvas.getContext('2d'),R=176,CX=300,CY=215;
const surface=document.createElement('canvas');surface.width=surface.height=R*2;
const surfaceCtx=surface.getContext('2d'),frame=surfaceCtx.createImageData(R*2,R*2),rays=[];
let texture=null,tw=0,th=0,showGrid=false,paintQueued=false;
for(let y=0;y<R*2;y++)for(let x=0;x<R*2;x++){
 const nx=(x+.5-R)/R,ny=(R-y-.5)/R,d=nx*nx+ny*ny;
 if(d<=1){const nz=Math.sqrt(1-d);rays.push({i:(y*R*2+x)*4,x:nx,y:ny,z:nz,light:.5+.5*Math.max(0,-.32*nx+.42*ny+.85*nz),alpha:Math.min(1,(1-Math.sqrt(d))*R)*255});}
}
function project(lat,lon){
 const a=lat*Math.PI/180,b=(lon-angle)*Math.PI/180,t=tilt*Math.PI/180;
 const x=Math.cos(a)*Math.sin(b),y=Math.sin(a),z=Math.cos(a)*Math.cos(b);
 return {x:CX+R*x,y:CY-R*(y*Math.cos(t)-z*Math.sin(t)),visible:y*Math.sin(t)+z*Math.cos(t)>.035};
}
function paint(){if(paintQueued)return;paintQueued=true;requestAnimationFrame(()=>{paintQueued=false;renderGlobe()});}
function renderGlobe(){
 ctx.clearRect(0,0,600,440);
 const sky=ctx.createRadialGradient(300,210,70,300,210,370);sky.addColorStop(0,'#17384a');sky.addColorStop(1,'#041321');ctx.fillStyle=sky;ctx.fillRect(0,0,600,440);
 for(let i=0;i<62;i++){ctx.fillStyle=i%3?'#b5c5d450':'#edf6ff99';ctx.fillRect((i*137+19)%600,(i*83+31)%440,i%7===0?2:1,1);}
 ctx.save();ctx.shadowColor='#48b8ff88';ctx.shadowBlur=24;ctx.beginPath();ctx.arc(CX,CY,R+1,0,Math.PI*2);ctx.fillStyle='#438db7';ctx.fill();ctx.restore();
 if(texture){
  const t=tilt*Math.PI/180,ct=Math.cos(t),st=Math.sin(t),rad=angle*Math.PI/180;
  for(const ray of rays){
   const wy=ray.y*ct+ray.z*st,wz=ray.z*ct-ray.y*st;
   const latitude=Math.asin(Math.max(-1,Math.min(1,wy))),longitude=Math.atan2(ray.x,wz)+rad;
   const u=((longitude/(2*Math.PI)+.5)%1+1)%1,v=.5-latitude/Math.PI;
   const ti=(Math.min(th-1,Math.max(0,Math.floor(v*th)))*tw+Math.floor(u*tw))*4,i=ray.i;
   let r=texture[ti],g=texture[ti+1],b=texture[ti+2];
   if(effect!==null){const value=45+effect-12*Math.abs(latitude)/(Math.PI/2),color=value>=55?[66,191,122]:value>=43?[236,186,72]:[231,115,77];r=r*.56+color[0]*.44;g=g*.56+color[1]*.44;b=b*.56+color[2]*.44;}
   frame.data[i]=r*ray.light;frame.data[i+1]=g*ray.light;frame.data[i+2]=b*ray.light;frame.data[i+3]=ray.alpha;
  }
  surfaceCtx.putImageData(frame,0,0);ctx.drawImage(surface,CX-R,CY-R);
 }else{ctx.beginPath();ctx.arc(CX,CY,R,0,Math.PI*2);ctx.fillStyle='#226693';ctx.fill();ctx.fillStyle='white';ctx.textAlign='center';ctx.font='16px system-ui';ctx.fillText('지구 표면을 준비하고 있어요…',CX,CY);}
 if(showGrid){ctx.strokeStyle='#dbf2ff40';ctx.lineWidth=.7;
  const line=points=>{ctx.beginPath();let pen=false;for(const [a,b] of points){const p=project(a,b);if(!p.visible){pen=false;continue;}pen?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y);pen=true;}ctx.stroke();};
  for(let a=-60;a<=60;a+=30)line(Array.from({length:181},(_,i)=>[a,i*2-180]));
  for(let b=-180;b<180;b+=30)line(Array.from({length:91},(_,i)=>[i*2-90,b]));
 }
 ctx.beginPath();ctx.arc(CX,CY,R+.7,0,Math.PI*2);ctx.strokeStyle='#98d9ff8c';ctx.lineWidth=1.5;ctx.stroke();
 countries.forEach(c=>{const p=project(c.lat,c.lon);if(!p.visible)return;ctx.beginPath();ctx.arc(p.x,p.y,c===selected?7:4.5,0,Math.PI*2);ctx.fillStyle=c===selected?'#ffd16a':'#f6fcff';ctx.strokeStyle='#174b58';ctx.lineWidth=2;ctx.fill();ctx.stroke();ctx.font=(c===selected?'bold ':'')+'14px system-ui';ctx.textAlign='center';ctx.lineWidth=4;ctx.strokeStyle='#071c2de6';ctx.strokeText(c.name,p.x,p.y-13);ctx.fillStyle='#fff';ctx.fillText(c.name,p.x,p.y-13);});
}
const earthImage=new Image();
earthImage.onload=()=>{const c=document.createElement('canvas');c.width=1536;c.height=768;const context=c.getContext('2d',{willReadFrequently:true});context.drawImage(earthImage,0,0,c.width,c.height);tw=c.width;th=c.height;texture=context.getImageData(0,0,tw,th).data;paint();};
earthImage.onerror=()=>{$('message').textContent='지구 이미지 로드에 실패했어요. 파일을 다시 열어 주세요.';};
earthImage.src='__EARTH_IMAGE__';
$('grid-toggle').onclick=()=>{showGrid=!showGrid;$('grid-toggle').setAttribute('aria-pressed',String(showGrid));$('grid-toggle').textContent=showGrid?'위·경도선 숨기기':'위·경도선 보기';paint();};
$('home-globe').onclick=()=>{angle=selected?selected.lon:120;tilt=selected?Math.max(-45,Math.min(45,selected.lat*.6)):12;paint();};
let start=null,moved=false;
canvas.onpointerdown=e=>{start={x:e.clientX,y:e.clientY,angle,tilt};moved=false;canvas.setPointerCapture(e.pointerId);};
canvas.onpointermove=e=>{if(!start)return;const dx=e.clientX-start.x,dy=e.clientY-start.y,scale=600/canvas.getBoundingClientRect().width;if(Math.hypot(dx,dy)>5)moved=true;angle=start.angle-dx*.35*scale;tilt=Math.max(-75,Math.min(75,start.tilt+dy*.25*scale));paint();};
canvas.onpointerup=e=>{if(!start)return;start=null;if(moved)return;const r=canvas.getBoundingClientRect(),x=(e.clientX-r.left)*600/r.width,y=(e.clientY-r.top)*440/r.height;const candidates=countries.map((c,i)=>({i,p:project(c.lat,c.lon)})).filter(c=>c.p.visible).sort((a,b)=>Math.hypot(a.p.x-x,a.p.y-y)-Math.hypot(b.p.x-x,b.p.y-y));if(candidates.length&&Math.hypot(candidates[0].p.x-x,candidates[0].p.y-y)<20)selectCountry(candidates[0].i);else $('message').textContent='나라 표시점이나 아래 나라 버튼을 눌러 주세요.';};
canvas.onpointercancel=()=>{start=null;};paint();
</script></body></html>
'''
s=s.replace('__EARTH_IMAGE__','data:image/jpeg;base64,'+base64.b64encode(Path('earth-texture.jpg').read_bytes()).decode())
p.write_text(s,encoding='utf-8')
print('Saved index.html:',p.stat().st_size,'bytes; expanded country cards:',len(data)*4)
