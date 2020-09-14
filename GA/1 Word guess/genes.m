
function[popelement]=genes(targetLength)
%  popelement=[];
%  for i=1:targetLength;

    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_';
    %find number of random characters to choose from
    numRands = length(s); 
    %generate random string
    popelement= s(ceil(rand(1,targetLength)*numRands));
end

    

    function[mutation]= newchar()
    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-';
    %find number of random characters to choose from
    numRands = length(s); 
    mutation=s(ceil(rand(1,1)*numRands)); %Generate a random mutation character from s
    end
    
    %   end