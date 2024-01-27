select a.codusur || ' - ' || c.nome RCA,
       a.numped,a.codcli,cli.cliente,a.codprod,b.codfornec,b.descricao,TRUNC((a.qtcorte/a.qtant)*100,2) || '%' "%",a.qtant "Qtd. Pedido",a.qtcorte "Qtd. Corte"
    from pccortefv a
    join pcprodut b on a.codprod = b.codprod
    join pcusuari c on a.codusur = c.codusur
    join pcclient cli on cli.codcli = a.codcli
where a.dtcorte > SYSDATE-1
    and b.codfornec = 588
    and b.codprod in (18170,18173,18584,18585,17883,17885,17884,18057,18058,18159)
    --and a.codusur in (155)
    --and a.codprod in (17474,17464,17467,17948,17950,17855)
order by  "Qtd. Corte" desc
