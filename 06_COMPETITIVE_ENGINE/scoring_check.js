"use strict";
function checkScenario(input) {
  // A deliberately restricted scoring calculation, not a game simulator.
  const fail = reason => ({status:"rejected",reason,scope:"conditional scoring only"});
  if(input.ruleset!=="core_2026-10-09" || input.mode!=="1v1_duel" || input.victory_score!==8 || !Array.isArray(input.battlefields) || input.battlefields.length!==2 || new Set(input.battlefields).size!==2) return fail("unsupported ruleset or mode");
  const players=input.players;
  if(!Array.isArray(players)||players.length!==2||new Set(players).size!==2||players.some(p=>typeof p!=="string"))return fail("exactly two players required");
  const scores={...input.start_scores};
  if(players.some(p=>!Number.isInteger(scores[p])||scores[p]<0||scores[p]>=8))return fail("invalid start score");
  if(input.assumptions?.no_point_modifiers!==true||input.assumptions?.no_unresolved_effects!==true||input.assumptions?.draw_available!==true||input.assumptions?.no_other_scoring!==true)return fail("unverified assumptions or unsupported interactions");
  let turn=input.start_turn, scored=new Set(input.already_scored??[]), winner=null;
  if(!players.includes(turn)||[...scored].some(b=>!input.battlefields.includes(b)))return fail("invalid turn or field");
  const trace=[];
  for(const e of input.events??[]){
    if(winner)return fail("event after victory");
    if(e.kind==="next_scoring_step"){
      if(e.player===turn||!players.includes(e.player)||e.phase!=="beginning_scoring"||e.intervening_events_abstracted!==true)return fail("invalid abstract turn transition");
      turn=e.player; scored=new Set();trace.push({kind:e.kind,player:turn,scope:"asserted boundary; earlier actions not replayed"});continue;
    }
    if(e.kind==="cleanup"){
      const eligible=players.filter(p=>scores[p]>=8&&players.every(q=>q===p||scores[p]>scores[q]));
      if(eligible.length===1)winner=eligible[0];
      trace.push({kind:e.kind,scores:{...scores},winner});continue;
    }
    if(!["hold","conquer"].includes(e.kind)||e.player!==turn||!input.battlefields.includes(e.field)||e.control_established_or_maintained!==true)return fail("unsupported scoring event or missing control premise");
    if(e.kind==="hold"&&e.phase!=="beginning_scoring")return fail("hold outside beginning scoring");
    if(scored.has(e.field))return fail("battlefield already scored this turn");
    scored.add(e.field);
    const drawInstead=e.kind==="conquer"&&scores[turn]>=7&&scored.size!==2;
    if(!drawInstead)scores[turn]++;
    trace.push({kind:e.kind,player:turn,field:e.field,points_gained:drawInstead?0:1,cards_drawn:drawInstead?1:0,scores:{...scores},scored:[...scored]});
  }
  return {status:"conditional_scoring_checked",scope:"1v1 scoring arithmetic only; asserted controls, no card effects, no legal deck or full replay certified",scores,winner,trace,full_replay:false};
}
if(typeof module!=="undefined")module.exports={checkScenario};
