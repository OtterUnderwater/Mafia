import { EliminationReasonEnum, RoleEnum, StatusEnum } from '@/custom_types/enums.ts';

export interface Player {
  id: number;
  nickname: string;
  fouls: number;
  role: RoleEnum;
  status: StatusEnum;
  elimination_reason: EliminationReasonEnum | null;
  idPS: number;
}

export interface JwtPayload {
  type: string;
  sub: string;
  username: string;
  exp: number;
  iat: number;
}
