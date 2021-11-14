function simulate
    
    TRANSITION = ['START', 'CHANGE', 'END'];
    PLACE = ['WAIT', 'INSIDE', 'DONE', 'FREE', 'BUSY', 'DOCU'];
    
    ADJACENCY = -[1 -1  0 1 -1  0;...
                  0  1 -1 0  1 -1;...
                 -1  0  0 0  0  1];
    RM = zeros(0,0); disp(ADJACENCY);
    XX = Disp_gr(ADJACENCY', RM);
    disp(XX);
end

function [pns] = DEFINE_PETRI_NET()
    pns.PN_NAME = 'CONSULTING MEDICAL SPECIALISTS';
    pns.set_of_Ps = {'WAIT', 'INSIDE', 'DONE', 'FREE', 'BUSY', 'DOCU'};
    pns.set_of_Ts = {'START', 'CHANGE', 'END'};
    pns.set_of_As = {'FREE', 'START', 1, 'WAIT', 'START', 1, 'START', 'INSIDE', 1, 'START', 'BUSY', 1, 'INSIDE', 'CHANGE', 1, ...
                     'BUSY', 'CHANGE', 1, 'CHANGE', 'DONE', 1, 'CHANGE', 'DOCU', 1, 'DOCU', 'END', 1, 'END', 'FREE', 1};
end