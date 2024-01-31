select a.codpromocao, 
        f.descricao,
        f.dtinicio, 
        f.dtfim, 
        a.numped, 
        a.data, 
        a.codcli, 
        substr(b.cliente,1,15) as Cliente, 
        D.CODSUPERVISOR SUP,
        A.CODUSUR || ' - ' ||
        SUBSTR(
            C.NOME,
            INSTR(C.NOME, ' ') + 1,
            INSTR(C.NOME, ' ', INSTR(C.NOME, ' ') + 1) - INSTR(C.NOME, ' ') - 1
        ) AS RCA, -- EXTRAI O NOME 
        a.qt as Quantidade,
        (a.pvenda*(a.qt)) as Valor
from pcpedi a, pcclient b, pcusuari c, pcsuperv d, pcbrindeex f, pcbrindeexpremio g, pcprodut h
where  a.codcli = b.codcli
and    a.codusur = c.codusur
and    c.codsupervisor = d.codsupervisor
and    a.codpromocao = f.codbrex
and    a.codpromocao = g.codbrex
and    g.codprod = h.codprod
--and    a.codpromocao in (:codpromo)
and    a.data  between '31-JAN-2024' and SYSDATE
--and    a.posicao in (:posicao)
and    h.codfornec in (:fornecedor)
and    a.codpromocao is not null

group by a.codpromocao, f.descricao,f.dtinicio, f.dtfim, a.qt,(a.pvenda*(a.qt)), a.numped, a.data, a.codcli, b.cliente, d.nome, a.codusur, c.nome, D.CODSUPERVISOR
order by a.numped,a.data
