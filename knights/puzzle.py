from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."

knowledge0 = And(
    Biconditional(AKnave, Not(AKnight)), Biconditional(AKnight, And(AKnave, AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Biconditional(AKnave, Not(AKnight)), # A is either a knight or knave
    Biconditional(BKnave, Not(BKnight)), # B is either a knight or knave
    Biconditional(AKnight, And(AKnave, BKnave)) 
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Biconditional(AKnave, Not(AKnight)), # A is either a knight or knave
    Biconditional(BKnave, Not(BKnight)), # B is either a knight or knave
    Biconditional(AKnight, Biconditional(AKnight, BKnight)),
    Biconditional(BKnight, Not(Biconditional(AKnight, BKnight)))

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

ASaidKnave = Symbol("A said 'I am a knave'")
knowledge3 = And(
    # A, B and C are knights or knaves but not both:
    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnave, Not(BKnight)),
    Biconditional(CKnave, Not(CKnight)),

    # If B is a knight, A said 'I am a knave', and C is a knave:
    
    Implication(BKnight, And(
      # A then said 'I am a Knave', A may be a Knight or a Knave:
      Implication(AKnight, AKnave),
      Implication(AKnave, Not(AKnave)),
      CKnave
    )),
    # If B is a knave, A said 'I am a knight' C is not a knave:
    
    Implication(BKnave, And(
      # A then said 'I am a Knight', A may be a Knight or a Knave:
      Implication(AKnight, AKnight),
      Implication(AKnave, Not(AKnight)),
      CKnight
    )),
    # If C is a knight, A is a knight:
    Implication(CKnight, AKnight),
    # If C is a knave, A is not a knight:
    Implication(CKnave, Not(AKnight))
)



def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
