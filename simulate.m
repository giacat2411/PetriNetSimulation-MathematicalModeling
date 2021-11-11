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