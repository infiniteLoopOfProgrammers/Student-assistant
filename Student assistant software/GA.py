import json
import random
from needFunction import create_checksum_json

class GA:
    def __init__(self, all_course,popSize):
        self.all_course = all_course
        self.popSize = popSize
        self.population = [self.random_schedule2() for _ in range(popSize)]
        
    def mutate(self,individual):
        individual_mutated = individual
        if random.random() < 1/self.popSize:
            index = random.randint(0, len(individual) - 1)
            # Get the Course_id of each object in individual_mutated
            individual_course_ids = [obj["Course_id"] for obj in individual_mutated]
            # Select courses that are not in individual_mutated
            available_courses = [course for course in self.all_course if course["Course_id"] not in individual_course_ids]
            if random.random() < 0.4 and available_courses:
                individual_mutated[index] = random.choice(available_courses)
            elif (random.random() < 0.7 or len(individual) < 2) and available_courses:
                individual_mutated.append(random.choice(available_courses))
            elif len(individual) > 1:
                individual_mutated.remove(individual_mutated[index]) 
        return individual_mutated

    @staticmethod
    def fitness(course_list, has_dormitory, isqochani):
        conflicts = 0
        # If the student has a high GPA, they might prefer more challenging classes
        # if gpa > 3.5:
        #     conflicts += len([c for c in schedule if c[0] in ['Math', 'Physics']])

        # If the student has a dormitory, they might prefer classes in the afternoon

        if not has_dormitory and not isqochani:
            for c in course_list:
                if "Time" in c and c["Time"] is not None:
                    for item in c["Time"]:
                        if item["Start_Time"] in ['12:00', '14:00']:
                            conflicts += 1
                            
        count_utils = sum(course["Units"] for course in course_list)
        if count_utils < 14:
            conflicts += (14 - count_utils)
        if count_utils > 20:
            conflicts += (count_utils - 20)
        # If the student prefers weekdays, they might not want classes on the weekend
        # if prefers_weekdays:
        #     conflicts += len([c for c in course_list if c[1] in ['14:00', '15:00']])

        return conflicts


    def random_schedule(course_list, target_sum):
        total_count = 0
        selected_classes = []
        course_list_copy = course_list.copy()

        while total_count < target_sum and course_list_copy:
            selected_class = random.choice(course_list_copy)
            if total_count + selected_class["Units"] <= target_sum:
                total_count += selected_class["Units"]
                selected_classes.append(selected_class)
                course_list_copy.remove(selected_class)

            if (target_sum-total_count) < min(course_list_copy, key=lambda x: x["Units"])["Units"]:
                break

        return selected_classes


    def random_schedule2(self):
        num_objects = random.randint(1, len(self.all_course))
        random_objects = random.sample(self.all_course, num_objects)
        return random_objects


    def select_parents(self, fitnesses):
        sum_of_fitnesses = sum(f for f in fitnesses)
        maxfitnesses = max(fitnesses) + 1
        probabilities=[(maxfitnesses-f)/(sum_of_fitnesses+1) for f in fitnesses]
        parents = [random.choices(self.population, weights=probabilities, k=1)[0] for _ in range(len(self.population))]
        return parents

    def crossover(self,parents):
        children = []
        for i in range(0, len(parents), 2):  # Step by 2 to get pairs of parents
            # Make sure there is a pair of parents
            if i + 1 < len(parents):
                parent1 = parents[i]
                parent2 = parents[i + 1]
                child1, child2 = GA.uniform_crossover(parent1, parent2)
                children.append(child1)
                children.append(child2)
        return children

    @staticmethod
    def uniform_crossover(parent1, parent2):
        # Make sure parent1 is the shorter list
        if len(parent1) > len(parent2):
            parent1, parent2 = parent2, parent1

        child1 = parent1.copy()
        child2 = parent2.copy()

        for i in range(len(parent1)):
            if random.random() < 0.5:  # 50% chance to swap each element
                if child1[i] not in child2 and child2[i] not in child1:
                    child1[i], child2[i] = child2[i], child1[i]
                else:
                    pass
                
        return child1, child2



if __name__ == "__main__":
    all_uniq_fitnesses = []
    all_uniq_course = []
    all_uniq_course_checksum = []    
    with open('json/dataGroup.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    for courses in data:    
        GAobj = GA(courses,10)

        best_individual = None
        for generation in range(500):
            # Evaluate the fitness of each individual in the population
            fitnesses = [GA.fitness(individual, False, False) for individual in GAobj.population]
            
            if best_individual is not None:
                max_index = fitnesses.index(max(fitnesses))
                fitnesses[max_index] = best_fitnesses
                GAobj.population[max_index] = best_individual
            best_fitnesses = min(fitnesses) 
            best_individual = GAobj.population[fitnesses.index(best_fitnesses)]
            
            # Select the best individuals to reproduce
            parents = GAobj.select_parents(fitnesses)
            
            children = GAobj.crossover(parents)
            # Create the next generation through crossover and mutation
            GAobj.population = [GAobj.mutate(individual) for individual in children]
        

        best_individual = GAobj.population[fitnesses.index(min(fitnesses))]    
        checksum = create_checksum_json(best_individual)
        if checksum not in all_uniq_course_checksum:
            all_uniq_course.append(best_individual)
            all_uniq_fitnesses.append(GA.fitness(best_individual, False, False))
            all_uniq_course_checksum.append(checksum)
    # The best individual is the one with the highest fitness
    min_fitnesses = min(all_uniq_fitnesses)
    best_individuals = [all_uniq_course[i] for i in range(len(all_uniq_course)) if GA.fitness(all_uniq_course[i], False, False) == min_fitnesses]
    fitnesses = [GA.fitness(individual, False, False) for individual in best_individuals]
    with open('out/best_individuals.json', 'w', encoding='utf-8') as f:
        json.dump(best_individuals, f, ensure_ascii=False)
