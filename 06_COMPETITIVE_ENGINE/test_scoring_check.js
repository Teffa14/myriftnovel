"use strict";
const assert=require("node:assert/strict");
const {checkScenario}=require("./scoring_check.js");
const fixture=require("./cases/CH01_SCORING_OPTION.json");
const clone=x=>JSON.parse(JSON.stringify(x));
function test(name,mutate,expect){const x=clone(fixture);mutate(x);assert.ok(expect(checkScenario(x)),name);}
test("last conquer draws, next hold wins",()=>{},r=>r.winner==="June"&&r.scores.Nico===7&&r.scores.June===8&&r.trace[0].cards_drawn===1);
test("second battlefield allows final conquer",x=>{x.already_scored=["B"];x.events=x.events.slice(0,2)},r=>r.winner==="Nico"&&r.scores.Nico===8);
test("ordinary conquer scores",x=>{x.start_scores.Nico=6;x.events=x.events.slice(0,2)},r=>r.scores.Nico===7&&r.winner===null);
test("duplicate field rejected",x=>{x.events.splice(1,0,clone(x.events[0]))},r=>r.status==="rejected");
test("hold in wrong phase rejected",x=>{x.events[3].phase="main"},r=>r.status==="rejected");
test("unresolved effects rejected",x=>{x.assumptions.no_unresolved_effects=false},r=>r.status==="rejected");
test("unsupported 2v2 rejected",x=>{x.mode="2v2"},r=>r.status==="rejected");
test("no actions after cleanup victory",x=>{x.already_scored=["B"]},r=>r.status==="rejected");
test("unknown battlefield rejected",x=>{x.events[0].field="C"},r=>r.status==="rejected");
test("no draw availability rejected",x=>{x.assumptions.draw_available=false},r=>r.status==="rejected");
console.log("10 conditional scoring tests passed");
