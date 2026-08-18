def evaluate_mtf_confluence(m15_bias, h1_trend, h4_trend):
    bias=(m15_bias or "NONE").upper(); h1=(h1_trend or "NONE").upper(); h4=(h4_trend or "NONE").upper()
    h1a=h1==bias; h4a=h4==bias; opp1=bias in ("BULLISH","BEARISH") and h1 not in (bias,"NONE","NEUTRAL"); opp4=bias in ("BULLISH","BEARISH") and h4 not in (bias,"NONE","NEUTRAL")
    count=int(h1a)+int(h4a)
    return {"confirmed":count>0,"blocked":opp4,"strength":("STRONG" if count==2 else "MODERATE" if count==1 else "WEAK"),"m15_bias":bias,"h1_trend":h1,"h4_trend":h4,"h1_aligned":h1a,"h4_aligned":h4a,"opposite_h1":opp1,"opposite_h4":opp4,"alignment_count":count}
