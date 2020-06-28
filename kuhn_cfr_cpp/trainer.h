#include <string>
#include <map>
#include "node.h"

class Trainer
{
public:
    Trainer() {}
    void Train(int p_iterations);
    double cfr(int p_cards[2], const std::string &p_history, double p_cfReachProbability[2]);

private:
    std::map<std::string, Node*> m_nodeMap;
};
