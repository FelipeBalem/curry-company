
import streamlit as st



#======================================
# STREAMLIT
#=======================================
#streamlit run nome-arquivo.py
#Lendo o arquivo

def main() -> None:
        
    #Mudando o layout da página para WIDE
    st.set_page_config(page_title= 'Curry Company - Home', layout = 'wide')
    
    
    
    #--------------------------------------------
    # BODY
    #--------------------------------------------
    
    st.write("# Bem vindo ao Dashboard da Curry Company! 👋")
    
    st.sidebar.success("Selecione uma visão acima.")
    
    st.markdown(
        """
        Esse dashboard contém vários gráficos e tabelas apresentando os resultados do nosso marketplace.
        **👈 Selecione uma visão na barra lateral ao lado** para ver nossas métricas.
        - Manipule os filtros na sidebar A VONTADE, todo o sistema é dinamizado para atender aos filtros.
        - **TODO** o código é escrito através de pesquisa em documentações e não copiado e colado;
        - Apesar de ser um sistema para treinamento de ciência de dados, com dados fictícios, ele é modularizado (no limite que o streamlit permite), e é ÚNICO;
        - Foi seguido um passo a passo dos instrutores para montagem do conceito, entretanto toda a programação foi realizada sem 'copia e cola' e foi melhorada em relação à original.
        - A intenção é mostrar minhas habilidades como desenvolvedor python (4 meses de estudos) e cientista de dados (1 mês de estudos) até o momento de completar esse sistema.
        - Os códigos e textos estão em inglês para demonstrar meu nível no idioma.
        - Neste projeto não é utilizado banco de dados, apenas uma tabela do excel.
        - Conforme for desenvolvendo outras soluções, serão acrescentadas aqui, mas você também pode acessar meu portfólio.
        ### Quer saber mais?
        - Veja os códigos [no GIT](https://streamlit.io)
        
        ### Contatos:
        - Envie uma mensagem para [felipe.balem.si@gmail.com](mailto:felipe.balem.si@gmail.com)
        - Explore meu portfólio no [Github](https://github.com/streamlit/demo-uber-nyc-pickups)
        - Acesse meu [LinkedIn](https://linkedin.com/prof-felipe-balem)
        - Não possuo outras redes sociais.
    """
    )


if __name__ == '__main__':
    main()