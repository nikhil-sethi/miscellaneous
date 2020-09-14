clear all 

% function[population]=popuation
pop_size=2000;
target=('nikhil_sethi');
targetLength=length(target);
mutationrate=0.01;
Generations=100;
count=1;


%INITIALISATION
%Generate new population of n elements by calling the genes function for each element
    for i=1:pop_size;
        population(i)=cellstr(genes(targetLength));%converting the charcter array in genes to a string element for storing in the population array
        
    end
    
% Calculate fitness
                %    FITNESS FUNCITON
            fitval=zeros(1,pop_size); fitness=zeros(1,pop_size);
        for i=1:pop_size;
            for t=1:targetLength;
             genome=char(population(i)); % convert string cell to character array 
                if genome(t)==target(t)
                fitval(i)=fitval(i)+1;
                fitness(i)=fitval(i)/targetLength;
                end
            end  
        end

    a=min(fitness);
    b=max(fitness);
    fitnessnorm=(fitness-a)/(b-a); %mapping the fitnesss array to (0,1) for normalisation
%     avgfitness(g)=sum(fitness)*100/pop_size;




    FitnessTable=table(zeros(1,Generations)',zeros(1,Generations)','VariableNames',{'Generations' 'Average_Fitness'});
    Generation=linspace(1,Generations,Generations); 
 for g=1:Generations
   % SELECTION
    % Creating the mating pool
        n=zeros(1,pop_size);
        matingpool=population; %initialising variables before the loop
        for i=1:pop_size;
          n=floor(fitnessnorm*100);
          for j=1:n(i);
              matingpool(end+1)=population(i); %adding the good scoring elements to the parental array same no. of times as their normalised probability
         
          end  
          j;
        end

   
    %child=[]; newpop=[];
    for i=1:pop_size;
        
         %REPRODUCTION
    % crossover
       mpl=length(matingpool);
       parenta= char(matingpool(ceil(rand(1,1)*mpl)));
       parentb= char(matingpool(ceil(rand(1,1)*mpl))); 
        offsprings(i)=cellstr(strcat(parenta(1:targetLength/2),parentb(targetLength/2+1:end)));

%         plot(avgfitness(i),Generation(i));
%      
%         hold on;
         
        %MUTATION
          s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';
            %find number of random characters to choose from
            numRands = length(s); 
            newchar=s(ceil(rand(1,1)*numRands));
            elementnum=ceil(mutationrate*targetLength);
            offspring=char(offsprings(i));
        for k=1:elementnum
             offspring(randi(numel(offspring)))=newchar;
        end
        offsprings(i)=cellstr(offspring);
        newpop(i)=offsprings(i);
    end
    
                    
    %ELITISM
    for i=1:pop_size
                 losers= newpop(fitnessnorm==0);
                winners=newpop(fitnessnorm==1);
                        for m=1: numel(losers)/2
                            losers(m)=winners(randi(numel(winners)));
                        end
                newpop(fitnessnorm==0)=losers;
    end   
                
                   population=newpop; 
        %EVALUATE GENERATION
         % Calculate fitness
            fitval=zeros(1,pop_size); fitness=zeros(1,pop_size);
        for i=1:pop_size;
            for t=1:targetLength;
             genome=char(population(i)); % convert string cell to character array 
                if genome(t)==target(t)
                fitval(i)=fitval(i)+1;
                fitness(i)=fitval(i)/targetLength;
                
                end
            end  
        end

    a=min(fitness);
    b=max(fitness);
    fitnessnorm=(fitness-a)/(b-a); %mapping the fitnesss array to (0,1) for normalisation
    avgfitness(g)=sum(fitness)*100/pop_size;
    FitnessTable(g,:)= table(g,avgfitness(g)) 
    
   % Check for best
%      if strcmp(newpop(i),target)==1 % compare target and current string 
%             msgbox(sprintf('You have reached your target phrase which is=%s at generation=%d',char(offsprings(i)),g))
%             maxfitval=0; maxfitness=0; 
%             for t=1:targetLength;
%              best=char(offsprings(i)); % convert string cell to character array 
%                 if best(t)==target(t)
%                 maxfitval=maxfitval+1;
%                 maxfitness=maxfitval/targetLength;
%                 end
%             end  
%             break;
%         end
%         max(fitness);
%      end
      
        
 end
%  FitnessTable
  plot(Generation,avgfitness,'-b');
     hold on;
     max(avgfitness);
   
% 



