from pathlib import Path
import re, json, hashlib, zipfile

root = Path(__file__).parent
original = Path(r'C:\Users\user\Downloads\index.html')
s = original.read_text(encoding='utf-8-sig')
s = s.replace('<title>지구본 속 선택</title>', '<title>지구본 속 선택 · 버전 2</title>')
s = s.replace('<header><h1>지구본 속 선택</h1><p>나라를 고르고, 나의 역할로 지구의 변화를 상상해 보세요.</p></header>', '<header><div class="eyebrow">EARTH CHOICES <span>VERSION 2</span></div><h1>지구본 속 선택</h1><p>하나의 지구, 서로 다른 선택.<br>8개 나라를 탐험하고 5가지 행동의 변화를 비교해 보세요.</p><div class="header-tags"><span>8개 나라</span><span>3가지 역할</span><span>역할마다 5가지 선택</span></div></header>')
css = '''
:root{--green:#17654d;--ink:#183d33}body{background:#eff5f1;background-image:radial-gradient(ellipse at top right,#d9eae1,transparent 60%);color:var(--ink)}header{padding-top:44px;padding-bottom:28px}h1{font-size:44px;letter-spacing:-2px;margin:10px 0}header>p{color:#526c60;font-size:18px;line-height:1.8}.eyebrow{font-size:14px;font-weight:750;letter-spacing:2px}.eyebrow span{letter-spacing:1px;background:#17654d;color:#fff;border-radius:30px;padding:6px 12px;margin-left:12px}.header-tags{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}.header-tags span{background:#fff9;border:1px solid #d1e2d7;padding:4px 12px;border-radius:30px;font-size:14px}.layout{grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start}.panel{box-shadow:0 9px 32px #214d3610;border-radius:24px;padding:26px}h2{font-size:22px}button{transition:background .15s,transform .15s}button:hover{transform:translateY(-1px)}.choices button{border-radius:15px;padding:18px;font-weight:650}.choices small,.choice-meta{font-weight:400}.choice-meta{grid-template-columns:1fr;gap:4px}.choice-meta b{min-width:44px}.cards details{border:1px solid #dfebe3;background:#f5f9f6}.cards details[open]{background:#edf6f0}details p{font-size:16px!important}.country-focus{border-left:3px solid #c59430;padding:14px 16px;background:#fff7e6;border-radius:0 12px 12px 0;margin:16px 0}.country-focus p{font-size:16px}.country-facts{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}.country-facts span{background:#e7f1eb;border-radius:8px;padding:4px 9px;font-size:14px}.impact{display:inline-block;padding:3px 9px;border-radius:7px;background:#e7f1eb;color:#245b46;font-size:14px;margin-top:10px}.history li{padding:12px 0;border-bottom:1px solid #deebe2;line-height:1.8}.role-tools{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0}.role-tools button{font-size:14px;padding:7px 10px}.sources a{color:#17654d}.sources{margin-top:20px;font-size:14px}.news h3{font-size:21px}.metrics .metric strong{font-size:26px}.study-prompt{background:#eef5f0;border-radius:12px;padding:14px;margin-top:16px}footer{max-width:1150px;margin:auto;padding:24px;color:#526c60;font-size:14px}@media(max-width:800px){h1{font-size:34px}.layout{grid-template-columns:1fr}header{padding-top:28px}.panel{padding:20px}}@media(prefers-reduced-motion:reduce){*{transition:none!important}}
'''
s = s.replace('</style>', css + '</style>')
extra = '''
// V2: 기존 국가 소개에 탐구 맥락과 생활 사례를 더합니다.
const countryExtras = [
 {facts:['동아시아','수도 서울','사계절'],more:['산지가 많고 삼면이 바다여서 산지·해안·도시의 생활 조건이 달라요. 같은 계절에도 지역별 날씨 차이를 살펴볼 수 있어요.','아파트와 상업 건물이 모인 지역에서는 여러 가구와 사업장이 함께 에너지를 사용해요. 개인의 절약과 건물 전체의 설비 개선을 비교해 보세요.','공동주택의 안내문이나 학교 활동처럼 함께 참여하는 방식도 있어요. 참여하기 쉬운 실천을 어떻게 알릴지 생각해 보세요.','반찬의 양을 조절하고 식재료를 나눠 쓰면 버려지는 음식을 줄일 수 있어요. 냉장고를 교체할 때는 효율과 폐기 냉매 처리를 함께 살펴보세요.'],focus:'도시의 냉난방과 오래된 가전제품을 주제로 탐구해요. 전기를 덜 쓰는 일과 냉매를 회수하는 일이 각각 어떤 문제에 연결될까요?',question:'아파트 한 동이 함께 참여한다면 개인의 선택은 어떻게 확산될까요?'},
 {facts:['동아시아','수도 베이징','넓은 지역 차이'],more:['해안과 내륙, 고원과 저지대의 조건이 달라요. 어느 지역을 기준으로 결정하는지 먼저 정하면 더 구체적으로 생각할 수 있어요.','제품을 만드는 공장뿐 아니라 보관 창고와 운송에도 에너지가 필요해요. 생산부터 소비까지 연결해서 살펴보세요.','설과 명절의 이동·소비 방식도 지역과 가정에 따라 달라요. 큰 행사에서 일회용품과 음식 낭비를 줄이는 방법을 토론해 보세요.','재료의 종류뿐 아니라 조리와 보관 방식도 중요해요. 지역 음식을 단순히 친환경 또는 비친환경이라고 나누기보다 운송과 낭비를 살펴보세요.'],focus:'산업 시설과 대규모 냉장 유통을 주제로 탐구해요. 한 곳의 시범 사업을 여러 지역에 적용하려면 무엇을 바꿔야 할까요?',question:'도시와 농촌에 똑같은 정책을 적용하면 어떤 어려움이 있을까요?'},
 {facts:['남아시아','수도 뉴델리','계절풍'],more:['비가 집중되는 시기와 건조한 시기의 차이는 농업과 생활용수에 영향을 줘요. 더위에 대응할 때 물과 전력을 함께 고려해 보세요.','냉방이 필요한 공간에서도 그늘·환기·단열 같은 방법을 함께 쓸 수 있어요. 모든 가정이 같은 설비를 살 수 있는 것은 아니에요.','다양한 언어로 정보를 제공하면 환경 교육에 참여하는 사람을 늘릴 수 있어요. 지역 공동체에 맞는 전달 방식을 생각해 보세요.','콩과 곡물을 활용하는 식단도 조리 연료와 보관 방식에 따라 에너지 사용이 달라져요. 음식의 종류와 처리 과정을 함께 관찰해 보세요.'],focus:'더운 날의 냉방 접근성과 에너지 절약을 함께 탐구해요. 건강을 지키면서 전력 부담을 줄일 방법을 찾아보세요.',question:'설비를 바꿀 여유가 적은 가정부터 지원하려면 어떻게 설계할까요?'},
 {facts:['북유럽','수도 오슬로','피오르 해안'],more:['바다와 산지가 있는 국토에서는 마을 간 이동 조건이 달라요. 높은 위도라고 해서 모든 지역의 기후가 같은 것은 아니에요.','전기를 어떻게 생산하는지와 얼마나 소비하는지는 서로 다른 질문이에요. 전력 생산뿐 아니라 건물의 열 손실과 산업 활동도 살펴보세요.','야외 활동을 즐길 때에도 이동 수단과 장비의 수명에 따라 자원 사용이 달라질 수 있어요. 지역과 원주민의 관점을 함께 고려해 보세요.','수산물의 보관에는 냉장·냉동이 중요해요. 식품 안전을 지키면서 누출을 줄이고 효율을 높이는 방법을 찾아보세요.'],focus:'추운 계절의 건물 효율과 수산물 냉장 유통을 탐구해요. 발전 방식이 달라도 냉매 관리는 왜 필요할까요?',question:'건물 단열과 냉장 설비 개선 중 어떤 사업부터 시작할까요?'},
 {facts:['북아메리카','수도 워싱턴 D.C.','다양한 기후'],more:['사막·해안·산지·평야의 환경 차이가 커요. 국가 전체를 하나의 기후로 가정하지 말고 구체적인 생활 장소를 떠올려 보세요.','자동차 이동이 필요한 지역과 대중교통이 편리한 지역의 선택 조건은 달라요. 개인의 실천이 가능하도록 시설을 마련하는 역할도 중요해요.','학교·도서관·지역 모임은 서로 다른 배경의 사람들이 환경 정보를 나누는 장소가 될 수 있어요. 한 가지 생활방식으로 일반화하지 않아요.','큰 냉장 창고부터 가정의 냉장고까지 식품 유통 단계가 이어져요. 적정량 구매와 냉매 관리가 각각 어떤 효과를 내는지 비교해 보세요.'],focus:'장거리 이동과 건물 냉난방을 탐구해요. 교통 여건이 다른 지역의 주민이 모두 참여할 수 있는 행동을 설계해 보세요.',question:'대중교통이 없는 지역에서는 어떤 대안을 제안할 수 있을까요?'},
 {facts:['남아메리카','수도 산티아고','남북으로 긴 국토'],more:['산맥과 바다 사이의 지형 때문에 지역 간 이동과 물 이용 조건이 달라요. 남북의 기후 차이를 정책에 반영하는 것이 중요해요.','광업과 농수산업에서는 전력뿐 아니라 물과 운송 조건도 살펴봐야 해요. 한 자원을 절약할 때 다른 부담이 생기는지도 생각해 보세요.','지역 공동체와 원주민의 생활 공간을 존중하는 협의가 필요해요. 설비를 놓는 위치를 정할 때 누구의 의견을 들어야 할까요?','신선 식품을 먼 곳에 보내려면 온도 관리가 필요해요. 음식물 손실을 줄이는 것과 냉장 설비의 부담을 함께 비교해 보세요.'],focus:'지역에 따라 다른 에너지·물 이용 조건을 탐구해요. 먼 지역의 냉매 회수 서비스를 어떻게 연결할 수 있을까요?',question:'회수 시설이 먼 지역의 운송 비용은 누가 부담하면 좋을까요?'},
 {facts:['동아프리카','수도 나이로비','적도와 고원'],more:['적도 부근이어도 높은 지역은 저지대와 기온이 달라요. 강수량과 물 이용 조건도 지역에 따라 다르다는 점을 기억해요.','수확한 농산물을 보관하고 시장에 운송하는 과정이 중요해요. 냉장 설비를 마련할 때 전력 공급과 유지보수도 함께 계획해야 해요.','환경 정보를 전달할 때 언어와 지역의 생활 경험을 고려해요. 주민이 직접 관리할 수 있는 방식인지 확인해 보세요.','식품을 적절히 보관하면 버려지는 양을 줄일 수 있어요. 냉장이 필요한 식품과 상온 보관이 가능한 식품의 조건을 구분해 보세요.'],focus:'농산물 보관과 지역별 전력 이용 조건을 탐구해요. 냉장 시설의 설치뿐 아니라 고장 수리와 냉매 관리까지 계획해 보세요.',question:'장비 지원이 끝난 뒤에도 계속 운영하려면 무엇이 필요할까요?'},
 {facts:['오세아니아','수도 캔버라','남반구'],more:['넓은 국토 안에서도 강수와 기온이 달라요. 건조한 내륙과 해안 도시를 같은 조건으로 생각하지 않도록 해요.','도시 밖에서는 이동과 설비 수리 거리가 길어질 수 있어요. 냉매 회수 거점과 전문 인력을 어디에 배치할지 생각해 보세요.','자외선 차단은 피부를 보호하는 행동이에요. 자외선 차단제를 바르는 것이 대기 중 오존층을 직접 회복시키는 것은 아니에요.','식품을 오래 보관하는 편리함과 냉장 설비의 전력 사용을 함께 살펴봐요. 냉매가 무엇인지 확인하고 폐기할 때 전문 회수처를 이용하는 방법을 배워요.'],focus:'더운 날의 냉방과 넓은 국토의 회수 체계를 탐구해요. 오존층 보호와 온실가스 감축에 필요한 행동을 구분해 보세요.',question:'멀리 떨어진 지역까지 전문 수거 서비스를 제공하려면 어떻게 해야 할까요?'}
];
countries.forEach((c,i)=>{c.extra=countryExtras[i];c.info=c.info.map((p,j)=>p+' '+c.extra.more[j]);});
const newActions = [
 [
 ['음식 낭비를 줄이는 일주일 계획 세우기','필요한 만큼 구매하고 남은 재료를 활용해요.',0,10,'가정의 식단 계획으로 음식 낭비 줄이기',{cost:'추가 지출 0원으로 가정',time:'계획 주 30분 · 4주 실천',effort:'보통 · 재고 확인과 식단 조절'}],
 ['냉매 종류 확인하고 전문가에게 점검 맡기기','오존층 파괴물질을 쓰는 오래된 설비를 가정하고 누출을 예방해요. 냉매를 직접 다루지 않아요.',12,5,'오래된 냉방 설비 점검 참여 확대',{cost:'점검 3~10만 원',time:'예약 1주 이내 · 점검 1시간',effort:'낮음 · 모델 확인과 전문업체 예약'}]
 ],
 [
 ['저온난화 냉매로 전환하는 시범 사업','HFC 설비를 가정해 기후 영향이 작은 대체 냉매와 안전 조건을 검토해요. HFC는 오존층을 파괴하지 않아요.',0,18,'기업, 냉매의 기후 영향 줄이기 착수',{cost:'시범 투자 1억 5,000만 원',time:'검토·설비 시험 6~9개월',effort:'높음 · 안전 검토와 전문 기술자 교육'}],
 ['반납 제품 수거와 부품 재사용 확대하기','오존층 파괴물질을 쓰는 구형 제품은 전문 회수하고, 쓸 수 있는 부품을 다시 활용해요.',15,12,'기업, 회수와 자원 순환 체계 확대',{cost:'초기 5,000만 원 · 운영 2,000만 원',time:'구축 3개월 · 지속 운영',effort:'보통 · 수거망과 품질 관리'}]
 ],
 [
 ['냉매 기술자 교육과 누출 점검 지원하기','오존층 파괴물질을 쓰는 구형 설비 관리와 안전한 회수·처리 교육을 지원해요.',20,10,'지역 기술자 교육과 냉매 관리 강화',{cost:'교육·점검 사업 20억 원',time:'준비 4개월 · 교육·점검 1년',effort:'높음 · 교육기관 및 사업장 협력'}],
 ['대중교통과 건물 단열 시범 사업 지원하기','이동과 냉난방에 필요한 에너지를 줄이고 참여하기 어려운 가구도 지원해요.',0,24,'지역 교통·건물 효율 개선 착수',{cost:'시범 사업 50억 원',time:'협의 1년 · 개선 2년',effort:'매우 높음 · 교통 계획과 공사 협의'}]
 ]
];
roles.forEach((r,i)=>{r.choices.splice(2,0,...newActions[i]);r.choices.forEach(c=>{c[6]=c[2]>0?'오존층 보호 중심':c[3]>0?'온실가스 감축 중심':'비교 기준';});});
'''
s=s.replace('const $=id=>',extra+'\nconst $=id=>')
s=s.replace("$('info').hidden=false;$('countryName')", "$('info').hidden=false;$('countryName')")
s=s.replace("$('cards').append(d)});", "$('cards').append(d);if(j===0)d.open=true;});const facts=document.createElement('div');facts.className='country-facts';selected.extra.facts.forEach(t=>{const x=document.createElement('span');x.textContent=t;facts.append(x)});$('cards').prepend(facts);const focus=document.createElement('div');focus.className='country-focus';const ft=document.createElement('strong');ft.textContent='이 나라에서 생각해 볼 환경 선택';const fp=document.createElement('p');fp.textContent=selected.extra.focus;focus.append(ft,fp);$('cards').append(focus);")
s=s.replace("button.append(description,meta);", "const badge=document.createElement('span');badge.className='impact';badge.textContent=c[6];button.append(description,badge,meta);")
s=s.replace("$('article').textContent=c[1]+' 아래 수치는", "$('article').textContent=c[1]+' '+selected.extra.focus+' 아래 수치는")
s=s.replace("$('choice-summary').textContent='선택한 행동의 가상 자원: '+resourceText(c);", "$('choice-summary').textContent='선택한 행동의 가상 자원: '+resourceText(c);$('reflection').textContent='함께 생각해요 · '+selected.extra.question;")
s=s.replace('<div id="metrics" class="metrics"></div>', '<div id="metrics" class="metrics"></div><p id="reflection" class="study-prompt"></p>')
s=s.replace('<div id="choices" class="choices"></div>', '<div id="role-tools" class="role-tools" hidden aria-label="역할 직접 선택"></div><div id="choices" class="choices"></div>')
s=s.replace("$('draw').onclick=drawRole;", "roles.forEach(r=>{const b=document.createElement('button');b.textContent=r.name+' 체험';b.onclick=()=>{clearTimeout(timer);timer=null;role=r;$('draw').hidden=true;$('draw').disabled=false;renderRole();showChoices()};$('role-tools').append(b)});function renderRole(){$('role').innerHTML='<h3>'+role.name+' 임명장</h3><p>'+role.resource+'</p><p class=\"muted\">'+selected.context+'</p>';[...$('role-tools').children].forEach((b,i)=>b.setAttribute('aria-pressed',String(roles[i]===role)));} $('draw').onclick=drawRole;")
s=s.replace("$('cost-note').hidden=true;resetResult();", "$('cost-note').hidden=true;$('role-tools').hidden=true;resetResult();")
s=s.replace("resetResult();$('choices').replaceChildren();$('cost-note').hidden=false;", "resetResult();renderRole();$('role-tools').hidden=false;$('choices').replaceChildren();$('cost-note').hidden=false;")
s=s.replace('냉매가 새지 않도록 회수·처리해요.', '오존층 파괴물질을 쓰는 구형 냉장고를 가정해 냉매를 전문 회수·처리해요.')
s=s.replace('설비와 폐기 제품의 냉매 관리를 개선해요.', '오존층 파괴물질을 쓰는 구형 설비와 폐기 제품의 냉매 관리를 개선해요.')
s=s.replace('관리 제도와 회수 기반 시설을 강화해요.', '오존층 파괴물질 관리 제도와 구형 설비의 냉매 회수 기반 시설을 강화해요.')
s=s.replace('</main>', '</main><footer>지구본 속 선택 · 버전 2 · 변유진<div class="sources">더 알아보기: <a href="https://ozone.unep.org/ozone-and-you" target="_blank" rel="noopener">UNEP 오존층 안내</a> · <a href="https://ozone.unep.org/kigali-amendment-implementation-begins" target="_blank" rel="noopener">HFC와 기후 변화</a> · <a href="https://www.un.org/climatechange/science/causes-effects-climate-change" target="_blank" rel="noopener">UN 기후 변화 원인과 영향</a></div><p>나라마다 다양한 삶이 있어요. 나라 소개는 학습용 요약이며 특정 국민의 생활을 대표하지 않아요.</p></footer>')
s=s.replace('이 예제는 냉매 관리와 회수를 오존층 보호 행동으로,', '냉매 종류에 따라 영향이 달라요. CFC·HCFC 같은 오존층 파괴물질의 누출 방지와 회수는 오존층 보호에, HFC 누출 감축은 기후 보호에 연결돼요. 이 앱은 구형 설비의 냉매 관리를 오존층 보호 행동으로,')
(root/'dist'/'index.html').write_text(s,encoding='utf-8')
(root/'README.txt').write_text('지구본 속 선택 V2\n\n실행: dist 폴더의 index.html을 브라우저로 여세요. 이미지가 포함되어 인터넷 없이 실행할 수 있습니다.\n원본 V1 파일은 변경하지 않았습니다.\n\n변경: 8개국 소개 확장, 환경 탐구 질문, 역할별 행동 5개(총 15개), 역할 직접 체험, 개선된 화면.\n효과·비용·시간은 가상 교육용 설정이며 실제 관측 또는 예측이 아닙니다.\n기록은 새로고침하면 사라집니다.\n',encoding='utf-8')
print('Created V2:',len(s),'characters; V1 SHA256:',hashlib.sha256(original.read_bytes()).hexdigest())
