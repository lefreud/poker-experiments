#include "trainer.h"
#include "time.h"
#include "constants.h"
#include <iostream>
#include <string>

void Trainer::Train(int p_iterations)
{
    int cards[] = {1, 2, 3};
    double utility = 0;
    srand(time(nullptr));
    for (size_t i = 0; i < p_iterations; i++)
    {
        // Shuffling
        for (int c1 = (sizeof(cards) / sizeof(int)) - 1; c1 > 0; c1--)
        {
            int c2 = rand() % (c1 + 1);
            int tmp = cards[c1];
            cards[c1] = cards[c2];
            cards[c2] = tmp;
        }

        double startingCfProbabilities[] = {1, 1};
        utility += cfr(cards, EMPTY_HISTORY, startingCfProbabilities);
    }
    std::cout << "Average game value:" << utility / p_iterations << std::endl;
    for (std::map<std::string, Node *>::iterator it = m_nodeMap.begin(); it != m_nodeMap.end(); it++)
    {
        std::cout << (it->second)->ToString() << std::endl;
    }
}
double Trainer::cfr(int p_cards[], const std::string &p_history, double p_cfReachProbability[2])
{
    int plays = p_history.length();
    int player = plays % 2;
    int opponent = 1 - player;

    // Terminal states
    if (plays > 1)
    {
        bool terminalPass = p_history.back() == 'p';
        bool doubleBet = p_history.substr(p_history.size() - 2) == "bb";
        bool playerCardHigher = p_cards[player] > p_cards[opponent];
        if (terminalPass)
        {
            if (p_history == "pp")
            {
                return playerCardHigher ? 1 : -1;
            }
            else
            {
                return 1;
            }
        }
        else if (doubleBet)
        {
            return playerCardHigher ? 2 : -2;
        }
    }

    std::string informationSet = std::to_string(p_cards[player]) + p_history;
    std::map<std::string, Node *>::iterator it = m_nodeMap.find(informationSet);
    Node *node = nullptr;
    if (it != m_nodeMap.end())
    {
        node = m_nodeMap[informationSet];
    }
    else
    {
        node = new Node(informationSet);
        m_nodeMap[informationSet] = node;
    }
    double *strategy = node->GetStrategy();
    node->UpdateCumulativeStrategy(strategy, p_cfReachProbability[player]);

    double actionUtilities[] = {0, 0};
    double nodeUtility = 0;
    for (size_t a = 0; a < NUM_ACTIONS; a++)
    {
        std::string nextHistory = p_history + ACTIONS[a];
        double nextCfReachProbability[] = {p_cfReachProbability[0], p_cfReachProbability[1]};
        if (player == 0)
        {
            nextCfReachProbability[0] *= strategy[a];
        }
        else
        {
            nextCfReachProbability[1] *= strategy[a];
        }
        actionUtilities[a] = -cfr(p_cards, nextHistory, nextCfReachProbability);
        nodeUtility += actionUtilities[a] * strategy[a];
    }
    for (size_t a = 0; a < NUM_ACTIONS; a++)
    {
        double regret = actionUtilities[a] - nodeUtility;
        double weigthedRegret = regret * p_cfReachProbability[1 - player];
        node->AccumulateActionRegrets(a, weigthedRegret);
    }
    delete[] strategy;
    return nodeUtility;
}
