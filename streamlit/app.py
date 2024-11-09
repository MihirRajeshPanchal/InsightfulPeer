import streamlit as st
from g1 import generate_response
import json
import groq

client = groq.Groq()

def main():
    st.set_page_config(page_title="C-o-T Peer Review", page_icon="🧠", layout="wide")
    
    st.title("Chain of Thought Reasoning Peer Review (Exhaustive or Trivial)")
    
    
    example_1 = '''This article applies the notion of “conceptors” – a form of regulariser introduced by the same author a few years ago, exhibiting appealing boolean logic pseudo-operations – to prevent forgetting in continual learning, more precisely in the training of neural networks on sequential tasks. [[INT-NEU, MET-NEU], [null]] It proposes itself as an improvement over the main recent development of the field, namely Elastic Weight Consolidation. [[RWK-NEU, OAL- NEU], [CMP-NEU]] After a brief and clear introduction to conceptors and their application to ridge regression, the authors explain how to inject conceptors into Stochastic Gradient Descent and finally, the real innovation of the paper, into Backpropagation. [[EXP-NEU, MET-NEU], [EMP-NEU]] Follows a section of experiments on variants of MNIST commonly used for continual learning. [[EXP-NEU], [EMP-NEU]] Continual learning in neural networks is a hot topic, and this article contributes a very interesting idea. [[PDI-POS], [NOV-POS]] The notion of conceptors is appealing in this particular use for its interpretation in terms of regularizer and in terms of Boolean logic. [[MET-POS, RES-POS], [EMP-POS]] The numeric examples, although quite toy, provide a clear illustration. [[ANA-POS], [PNF-POS]] A few things are still missing to back the strong claims of this paper: Some considerations of the computational costs: the reliance on the full N × N correlation matrix R makes me fear it might be costly, as it is applied to every layer of the neural networks and hence is the largest number of units in a layer. [[MET-NEG, ANA-NEG], [SUB-NEG]] This is of course much lighter than if it were the covariance matrix of all the weights, which would be daunting, but still deserves to be addressed, if only with wall time measures. [[MET-NEG], [SUB-NEG]] It could also be welcome to use a more grounded vocabulary, e.g. on p.2 Figure 1 shows examples of conceptors computed from three clouds of sample state points coming from a hypothetical 3-neuron recurrent network that was driven with input signals from three dif- ferent sources could be much more simply said as Figure 1 shows the ellipses corresponding to three sets of R3 points. [[DAT-NEU, MET-NEU, TNF-NEU], [SUB-NEU, EMP-NEU]] Being less grandiose would make the value of this article nicely on its own. [[OAL-NEU], [PNF-NEU]] Some examples beyond the contrived MNIST toy examples would be welcome. [[MET-NEU], [SUB-NEU]] For example, the main method this article is compared to (EWC) had a very strong section on Reinforcement learning examples in the Atari framework, not only as an illustration but also as a motivation. [[MET-POS], [EMP-POS]] I realize not every- one has the computational or engineering resources to try extensively on multiple benchmarks from classification to reinforcement learning. [[EXT-NEU], [SUB-NEG]] Nevertheless, with- out going to that extreme, it might be worth adding an extra demo on something bigger than MNIST. [[MET-NEU, ANA-NEU], [SUB-NEU]] The authors transparently explain in their answer that they do not (yet!) belong to the deep learning community and hope to find some collaborations to pursue this further. [[FWK-NEG], [IMP-NEG]] If I may make a suggestion, I think their work would get a much stronger impact by doing it the reverse way: first find- ing the collaboration, then adding this extra empirical results, which then leads to a bigger impact publication. [[FWK-NEU], [IMP-NEU]] The later point would normally make me attribute a score of ”6: Marginally above acceptance threshold” by current DL community standards, [[OAL-NEU], [IMP-NEU]] but because there is such a pressing need for methods to tackle this problem, and because this article can generate thinking along new lines about this, I give it a 7: Good paper, accept. [[MET-NEU, FWK-POS, OAL-POS], [NOV-POS, IMP-POS, REC-POS]]'''
    
    example_2 = '''
    This paper derived an upper bound on adversarial perturbation for neural networks with one
    hidden layer.[[INT-NEU], [null]] The upper bound is derived via (1) theorem of middle value;
    (2) replace the middle value by the maximum (eq 4); (3) replace the maximum of the gradient
    value (locally) by the global maximal value (eq 5); (4) this leads to a non-convex quadratic
    program, and then the authors did a convex relaxation similar to maxcut to upper bound the
    function by a SDP, which then can be solved in polynomial time.[[MET-NEU], [EMP-NEU]]
    The main idea of using upper bound (as opposed to lower bound) is reasonable.[[PDI-NEU],
    [null]] However, I find there are some limitations/weakness of the proposed method: 1. The
    method is likely not extendable to more complicated and more practical networks, beyond
    the ones discussed in the paper (ie with one hidden layer) 2.[[MET-NEG], [EMP-NEG]] SDP
    while tractable, would still require very expensive computation to solve exactly.[[MET-NEU],
    [EMP-NEU]] 3. The relaxation seems a bit loose - in particular, in above step 2 and 3, the
    authors replace the gradient value by a global upper bound on that, which to me seems can
    be pretty loose.”[[MET-NEG], [EMP-NEG]]
    
    '''

    
    user_query = st.text_input("Enter a Review Sentence ", placeholder="e.g., However, the paper is incomplete, with a very low number of references, only 2 conference papers if we assume the list is up to date.")

    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Exhaustive Review",key="example1"):
            user_query = example_1

    with col2:
        if st.button("Trivial Review",key="example2"):
            user_query = example_2

    if user_query:     
        st.write(f"Query: {user_query}")
        
        user_query += " Classify the following sentence as trivial or exhaustive ('Trivial' typically refers to something that is unimportant or lacking in significance, whereas 'exhaustive' implies a thorough or comprehensive treatment of a subject.) Give end result as Trivial or Exhaustive."
        
        st.write("Generating response...")
        
        response_container = st.empty()
        time_container = st.empty()
        
        for steps, total_thinking_time in generate_response(user_query, client):
            with response_container.container():
                for i, (title, content, thinking_time) in enumerate(steps):
                    
                    if not isinstance(content, str):
                        content = json.dumps(content)
                    if title.startswith("Final Answer"):
                        st.markdown(f"### {title}")
                        if '```' in content:
                            parts = content.split('```')
                            for index, part in enumerate(parts):
                                if index % 2 == 0:
                                    st.markdown(part)
                                else:
                                    if '\n' in part:
                                        lang_line, code = part.split('\n', 1)
                                        lang = lang_line.strip()
                                    else:
                                        lang = ''
                                        code = part
                                    st.code(part, language=lang)
                        else:
                            st.markdown(content.replace('\n', '<br>'), unsafe_allow_html=True)
                    else:
                        with st.expander(title, expanded=True):
                            st.markdown(content.replace('\n', '<br>'), unsafe_allow_html=True)
            
            if total_thinking_time is not None:
                time_container.markdown(f"**Total thinking time: {total_thinking_time:.2f} seconds**")

if __name__ == "__main__":
    main()