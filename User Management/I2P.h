// I2P.h
#ifndef I2P_H
#define I2P_H

#include <string>
#include <vector>

class UserManager {
 private:
  std::vector<std::string> MatNums;
 public:
  UserManager();

  int GetMatNum(const std::string& s);
  int GetYear(const std::string& filename);
  std::string PassGen();
  void TakeCSV(const std::string& filename);
  void CreateLinuxUser(const std::string& USERNAME, const std::string& PASSWORD, const std::string& YEAR);
  void DeleteLinuxUser(const std::string& USERNAME, const std::string& YEAR);
  void ManageUsers(const std::string& filename, int function);
};

#endif //I2P_H
